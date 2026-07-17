from database.db import Database
from models.workflow import Workflow


class WorkflowService:
    """
    Service layer for Workflow (Kanban) operations.
    """

    def __init__(self):
        self.db = Database()
        self.db.connect()

    # ==========================================
    # Get All Workflow Cards
    # ==========================================

    def get_all_workflow_tasks(self):
        """Fetch all tasks grouped by their current workflow stage."""
        query = """
            SELECT t.*, u.full_name AS assigned_name, p.project_name,
                   w.current_stage, w.previous_stage, w.updated_by AS wf_updated_by,
                   w.updated_at AS wf_updated_at
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            LEFT JOIN users u ON t.assigned_to = u.id
            LEFT JOIN workflows w ON t.id = w.task_id
            ORDER BY t.priority DESC, t.created_at DESC
        """
        return self.db.fetchall(query)

    def get_tasks_by_stage(self, stage):
        """Get tasks filtered by workflow stage."""
        query = """
            SELECT t.*, u.full_name AS assigned_name, p.project_name
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            LEFT JOIN users u ON t.assigned_to = u.id
            JOIN workflows w ON t.id = w.task_id
            WHERE w.current_stage = %s
            ORDER BY t.priority DESC, t.created_at DESC
        """
        return self.db.fetchall(query, (stage,))

    # ==========================================
    # Move Task to Next Stage
    # ==========================================

    def move_task(self, task_id, new_stage, user_id):
        """Move a task to a new workflow stage with validation."""
        # Get current workflow
        wf_query = "SELECT * FROM workflows WHERE task_id = %s"
        workflow = self.db.fetchone(wf_query, (task_id,))

        if not workflow:
            return {"success": False, "message": "Workflow entry not found."}

        current_stage = workflow["current_stage"]

        # Validate transition
        valid_transitions = Workflow.VALID_TRANSITIONS
        allowed = valid_transitions.get(current_stage, [])

        if new_stage not in allowed:
            return {
                "success": False,
                "message": f"Cannot move from '{current_stage}' to '{new_stage}'."
            }

        # Update workflow
        update_query = """
            UPDATE workflows
            SET previous_stage = %s, current_stage = %s,
                updated_by = %s, updated_at = CURRENT_TIMESTAMP
            WHERE task_id = %s
        """
        self.db.execute(update_query, (current_stage, new_stage, user_id, task_id))

        # Also update task status
        task_update = """
            UPDATE tasks
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        self.db.execute(task_update, (new_stage, task_id))

        # Log activity
        self._log_activity(user_id, f"Moved task ID {task_id} from '{current_stage}' to '{new_stage}'")

        return {"success": True, "message": f"Task moved to '{new_stage}'."}

    # ==========================================
    # Get Workflow History for a Task
    # ==========================================

    def get_workflow_history(self, task_id):
        """Get the workflow history for a task."""
        query = """
            SELECT w.*, u.full_name AS updated_by_name
            FROM workflows w
            LEFT JOIN users u ON w.updated_by = u.id
            WHERE w.task_id = %s
            ORDER BY w.updated_at DESC
        """
        return self.db.fetchall(query, (task_id,))

    # ==========================================
    # Log Activity Helper
    # ==========================================

    def _log_activity(self, user_id, action):
        """Insert an activity log entry."""
        try:
            query = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
            self.db.execute(query, (user_id, action))
        except Exception:
            pass