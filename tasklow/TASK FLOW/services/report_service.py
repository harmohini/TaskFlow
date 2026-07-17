from database.db import Database


class ReportService:
    """
    Service layer for generating reports and statistics.
    """

    def __init__(self):
        self.db = Database()
        self.db.connect()

    # ==========================================
    # Dashboard Stats
    # ==========================================

    def get_dashboard_stats(self):
        """Get all dashboard statistics."""
        total_projects = self._count("projects")
        total_tasks = self._count("tasks")

        pending_tasks = self._count_where("tasks", "status != 'Completed'")
        completed_tasks = self._count_where("tasks", "status = 'Completed'")
        high_priority = self._count_where("tasks", "priority IN ('High', 'Critical')")
        overdue = self._count_where("tasks", "due_date < CURRENT_DATE AND status != 'Completed'")

        return {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "high_priority": high_priority,
            "overdue_tasks": overdue
        }

    # ==========================================
    # Report Data
    # ==========================================

    def get_report_data(self):
        """Get data for Charts.js reports."""
        # Tasks by status
        status_data = self.db.fetchall("""
            SELECT status, COUNT(*) AS count
            FROM tasks
            GROUP BY status
            ORDER BY status
        """)

        # Tasks by priority
        priority_data = self.db.fetchall("""
            SELECT priority, COUNT(*) AS count
            FROM tasks
            GROUP BY priority
            ORDER BY priority
        """)

        # Tasks completed per month (last 12 months)
        monthly_data = self.db.fetchall("""
            SELECT
                TO_CHAR(date_trunc('month', created_at), 'Mon YYYY') AS month,
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
            FROM tasks
            WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY date_trunc('month', created_at)
            ORDER BY date_trunc('month', created_at)
        """)

        # Projects by status
        project_status = self.db.fetchall("""
            SELECT status, COUNT(*) AS count
            FROM projects
            GROUP BY status
            ORDER BY status
        """)

        total_tasks = self._count("tasks")
        completed_tasks = self._count_where("tasks", "status = 'Completed'")
        total_projects = self._count("projects")
        completed_projects = self._count_where("projects", "status = 'Completed'")

        completion_rate = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
        productivity = round((completed_projects / total_projects * 100), 1) if total_projects > 0 else 0

        return {
            "status_data": status_data,
            "priority_data": priority_data,
            "monthly_data": monthly_data,
            "project_status": project_status,
            "tasks_completed": completed_tasks,
            "tasks_pending": total_tasks - completed_tasks,
            "projects_completed": completed_projects,
            "productivity": productivity,
            "completion_rate": completion_rate
        }

    # ==========================================
    # Recent Activities
    # ==========================================

    def get_recent_activities(self, limit=10):
        """Fetch recent activity logs."""
        query = """
            SELECT a.*, u.full_name AS user_name
            FROM activity_logs a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.activity_time DESC
            LIMIT %s
        """
        return self.db.fetchall(query, (limit,))

    # ==========================================
    # Helper Methods
    # ==========================================

    def _count(self, table):
        """Get total count from a table."""
        # Validate table name to prevent SQL injection
        allowed_tables = ["projects", "tasks", "users", "activity_logs", "workflows", "project_members"]
        if table not in allowed_tables:
            raise ValueError(f"Invalid table name: {table}")
        
        result = self.db.fetchone(f"SELECT COUNT(*) AS total FROM {table}")
        return result["total"] if result else 0

    def _count_where(self, table, condition, params=None):
        """Get count with a condition."""
        # Validate table name to prevent SQL injection
        allowed_tables = ["projects", "tasks", "users", "activity_logs", "workflows", "project_members"]
        if table not in allowed_tables:
            raise ValueError(f"Invalid table name: {table}")
        
        query = f"SELECT COUNT(*) AS total FROM {table} WHERE {condition}"
        result = self.db.fetchone(query, params)
        return result["total"] if result else 0
