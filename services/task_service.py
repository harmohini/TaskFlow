from database.db import Database
from models.task import Task


class TaskService:
    """
    Service layer for Task CRUD operations.
    """

    def __init__(self):
        self.db = Database()
        self.db.connect()

    # ==========================================
    # Create Task
    # ==========================================

    def create_task(self, project_id, title, description, priority, due_date, assigned_to, user_id):
        """Create a new task and log activity."""
        query = """
            INSERT INTO tasks
            (project_id, title, description, priority, due_date, assigned_to, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (project_id, title, description, priority, due_date, assigned_to, "To Do")
        self.db.execute(query, values)

        # Create workflow entry
        task_id_query = "SELECT MAX(id) AS id FROM tasks"
        task_result = self.db.fetchone(task_id_query)
        new_task_id = task_result["id"] if task_result else None

        if new_task_id:
            wf_query = """
                INSERT INTO workflows (task_id, current_stage, updated_by)
                VALUES (%s, %s, %s)
            """
            self.db.execute(wf_query, (new_task_id, "To Do", user_id))

        self._log_activity(user_id, f"Created task '{title}'")

        return {"success": True, "message": "Task created successfully."}

    # ==========================================
    # Get Tasks For Project
    # ==========================================

    def get_tasks_by_project(self, project_id):
        """Get all tasks for a specific project."""
        query = """
            SELECT t.*, u.full_name AS assigned_name
            FROM tasks t
            LEFT JOIN users u ON t.assigned_to = u.id
            WHERE t.project_id = %s
            ORDER BY t.created_at DESC
        """
        return self.db.fetchall(query, (project_id,))

    # ==========================================
    # Get All Tasks
    # ==========================================

    def get_all_tasks(self, search="", status="", priority="", project_id=None):
        """Fetch tasks with optional filters."""
        query = """
            SELECT t.*, u.full_name AS assigned_name, p.project_name
            FROM tasks t
            LEFT JOIN users u ON t.assigned_to = u.id
            JOIN projects p ON t.project_id = p.id
            WHERE 1=1
        """
        values = []

        if search:
            query += " AND t.title ILIKE %s"
            values.append(f"%{search}%")

        if status:
            query += " AND t.status = %s"
            values.append(status)

        if priority:
            query += " AND t.priority = %s"
            values.append(priority)

        if project_id:
            query += " AND t.project_id = %s"
            values.append(project_id)

        query += " ORDER BY t.created_at DESC"

        return self.db.fetchall(query, values)

    # ==========================================
    # Get Task By ID
    # ==========================================

    def get_task_by_id(self, task_id):
        """Fetch a single task with joins."""
        query = """
            SELECT t.*, u.full_name AS assigned_name, p.project_name
            FROM tasks t
            LEFT JOIN users u ON t.assigned_to = u.id
            JOIN projects p ON t.project_id = p.id
            WHERE t.id = %s
        """
        return self.db.fetchone(query, (task_id,))

    # ==========================================
    # Update Task
    # ==========================================

    def update_task(self, task_id, title, description, priority, status, due_date, assigned_to, user_id):
        """Update task details and log activity."""
        query = """
            UPDATE tasks
            SET title = %s, description = %s, priority = %s,
                status = %s, due_date = %s, assigned_to = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        values = (title, description, priority, status, due_date, assigned_to, task_id)
        self.db.execute(query, values)

        self._log_activity(user_id, f"Updated task '{title}'")

        return {"success": True, "message": "Task updated successfully."}

    # ==========================================
    # Update Task Status Only
    # ==========================================

    def update_task_status(self, task_id, new_status, user_id):
        """Update only the status of a task."""
        query = """
            UPDATE tasks
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        self.db.execute(query, (new_status, task_id))

        self._log_activity(user_id, f"Changed task status to '{new_status}'")

        return {"success": True, "message": "Task status updated."}

    # ==========================================
    # Assign Task
    # ==========================================

    def assign_task(self, task_id, assigned_to, user_id):
        """Assign a task to a user."""
        query = "UPDATE tasks SET assigned_to = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        self.db.execute(query, (assigned_to, task_id))

        self._log_activity(user_id, f"Assigned task ID {task_id} to user ID {assigned_to}")

        return {"success": True, "message": "Task assigned successfully."}

    # ==========================================
    # Delete Task
    # ==========================================

    def delete_task(self, task_id, user_id):
        """Delete a task and log activity."""
        task = self.get_task_by_id(task_id)
        title = task["title"] if task else "Unknown"

        query = "DELETE FROM tasks WHERE id = %s"
        self.db.execute(query, (task_id,))

        self._log_activity(user_id, f"Deleted task '{title}'")

        return {"success": True, "message": "Task deleted successfully."}

    # ==========================================
    # Log Activity
    # ==========================================

    def _log_activity(self, user_id, action):
        """Insert an activity log entry."""
        try:
            query = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
            self.db.execute(query, (user_id, action))
        except Exception:
            pass