from database.db import Database
from models.project import Project
from models.activity import Activity


class ProjectService:
    """
    Service layer for Project CRUD operations.
    """

    def __init__(self):
        self.db = Database()
        self.db.connect()

    # ==========================================
    # Create Project
    # ==========================================

    def create_project(self, project_name, description, start_date, end_date, status, created_by, member_ids=None):
        """Create a new project, add creator as admin member, and log activity."""
        query = """
            INSERT INTO projects
            (project_name, description, start_date, end_date, status, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (project_name, description, start_date, end_date, status, created_by)
        self.db.execute(query, values)

        # Get the new project ID
        project_result = self.db.fetchone("SELECT MAX(id) AS id FROM projects")
        project_id = project_result["id"] if project_result else None

        # Add creator as admin member
        if project_id:
            self.add_member(project_id, created_by, "Admin")

            # Add additional members if provided
            if member_ids:
                for uid in member_ids:
                    if int(uid) != int(created_by):
                        self.add_member(project_id, int(uid), "Member")

        # Log activity
        self._log_activity(created_by, f"Created project '{project_name}'")

        return {"success": True, "message": "Project created successfully.", "project_id": project_id}

    # ==========================================
    # Get All Projects
    # ==========================================

    def get_all_projects(self, search="", status=""):
        """Fetch projects with optional search and status filter."""
        query = """
            SELECT p.*, u.full_name AS creator_name
            FROM projects p
            LEFT JOIN users u ON p.created_by = u.id
            WHERE 1=1
        """
        values = []

        if search:
            query += " AND p.project_name ILIKE %s"
            values.append(f"%{search}%")

        if status:
            query += " AND p.status = %s"
            values.append(status)

        query += " ORDER BY p.created_at DESC"

        return self.db.fetchall(query, values)

    # ==========================================
    # Get Project By ID
    # ==========================================

    def get_project_by_id(self, project_id):
        """Fetch a single project with stats."""
        query = """
            SELECT p.*, u.full_name AS creator_name
            FROM projects p
            LEFT JOIN users u ON p.created_by = u.id
            WHERE p.id = %s
        """
        return self.db.fetchone(query, (project_id,))

    def get_project_stats(self, project_id):
        """Get task statistics for a project."""
        total = self.db.fetchone(
            "SELECT COUNT(*) AS total FROM tasks WHERE project_id = %s",
            (project_id,)
        )
        completed = self.db.fetchone(
            "SELECT COUNT(*) AS total FROM tasks WHERE project_id = %s AND status = 'Completed'",
            (project_id,)
        )
        members = self.db.fetchall(
            """
            SELECT DISTINCT u.id, u.full_name
            FROM tasks t
            JOIN users u ON t.assigned_to = u.id
            WHERE t.project_id = %s AND t.assigned_to IS NOT NULL
            """,
            (project_id,)
        )
        total_count = total["total"] if total else 0
        completed_count = completed["total"] if completed else 0
        progress = round((completed_count / total_count * 100), 1) if total_count > 0 else 0

        return {
            "total_tasks": total_count,
            "completed_tasks": completed_count,
            "progress": progress,
            "members": members or []
        }

    # ==========================================
    # Update Project
    # ==========================================

    def update_project(self, project_id, project_name, description, start_date, end_date, status, user_id):
        """Update project details and log activity."""
        query = """
            UPDATE projects
            SET project_name = %s, description = %s, start_date = %s,
                end_date = %s, status = %s
            WHERE id = %s
        """
        values = (project_name, description, start_date, end_date, status, project_id)
        self.db.execute(query, values)

        self._log_activity(user_id, f"Updated project '{project_name}'")

        return {"success": True, "message": "Project updated successfully."}

    # ==========================================
    # Delete Project
    # ==========================================

    def delete_project(self, project_id, user_id):
        """Delete a project and log activity."""
        project = self.get_project_by_id(project_id)
        name = project["project_name"] if project else "Unknown"

        query = "DELETE FROM projects WHERE id = %s"
        self.db.execute(query, (project_id,))

        self._log_activity(user_id, f"Deleted project '{name}'")

        return {"success": True, "message": "Project deleted successfully."}

    # ==========================================
    # Project Members Management
    # ==========================================

    def get_project_members(self, project_id):
        """Get all members of a project with their roles."""
        query = """
            SELECT pm.*, u.full_name, u.email, u.role AS user_role
            FROM project_members pm
            JOIN users u ON pm.user_id = u.id
            WHERE pm.project_id = %s
            ORDER BY pm.joined_at ASC
        """
        return self.db.fetchall(query, (project_id,))

    def get_non_members(self, project_id):
        """Get users who are NOT members of a project."""
        query = """
            SELECT u.id, u.full_name, u.email
            FROM users u
            WHERE u.id NOT IN (
                SELECT user_id FROM project_members WHERE project_id = %s
            )
            ORDER BY u.full_name
        """
        return self.db.fetchall(query, (project_id,))

    def add_member(self, project_id, user_id, role="Member"):
        """Add a user as a member of a project."""
        query = """
            INSERT INTO project_members (project_id, user_id, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (project_id, user_id) DO NOTHING
        """
        self.db.execute(query, (project_id, user_id, role))

        # Log activity (if caller provides user_id for logging, it's different)
        # The route handler will log this activity with the current user's ID
        return {"success": True, "message": "Member added successfully."}

    def remove_member(self, project_id, user_id, logged_in_user_id):
        """Remove a user from a project."""
        # Get the member name for logging
        member_data = self.db.fetchone(
            "SELECT full_name FROM users WHERE id = %s",
            (user_id,)
        )
        member_name = member_data["full_name"] if member_data else "Unknown"

        query = """
            DELETE FROM project_members
            WHERE project_id = %s AND user_id = %s
        """
        self.db.execute(query, (project_id, user_id))

        self._log_activity(logged_in_user_id, f"Removed {member_name} from project")

        return {"success": True, "message": "Member removed successfully."}

    def update_member_role(self, project_id, user_id, new_role, logged_in_user_id):
        """Update a member's role within a project."""
        query = """
            UPDATE project_members
            SET role = %s
            WHERE project_id = %s AND user_id = %s
        """
        self.db.execute(query, (new_role, project_id, user_id))

        self._log_activity(logged_in_user_id, f"Updated member role in project")

        return {"success": True, "message": "Member role updated."}

    # ==========================================
    # Log Activity
    # ==========================================

    def _log_activity(self, user_id, action):
        """Insert an activity log entry."""
        query = "INSERT INTO activity_logs (user_id, action) VALUES (%s, %s)"
        self.db.execute(query, (user_id, action))
