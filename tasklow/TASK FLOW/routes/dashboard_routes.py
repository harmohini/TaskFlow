from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from services.report_service import ReportService

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

report_service = ReportService()


# ------------------------------------------
# Dashboard
# ------------------------------------------

@dashboard_bp.route("/dashboard")
def dashboard():
    """Render the main dashboard with statistics."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    stats = report_service.get_dashboard_stats()
    recent_projects = report_service.db.fetchall(
        """
        SELECT *
        FROM projects
        ORDER BY created_at DESC
        LIMIT 5
        """
    )
    recent_tasks = report_service.db.fetchall(
        """
        SELECT tasks.*, projects.project_name
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        ORDER BY tasks.created_at DESC
        LIMIT 5
        """
    )
    recent_activities = report_service.get_recent_activities(8)

    return render_template(
        "dashboard.html",
        total_projects=stats["total_projects"],
        total_tasks=stats["total_tasks"],
        completed_tasks=stats["completed_tasks"],
        pending_tasks=stats["pending_tasks"],
        high_priority=stats["high_priority"],
        overdue_tasks=stats["overdue_tasks"],
        projects=recent_projects,
        tasks=recent_tasks,
        activities=recent_activities
    )


# ------------------------------------------
# Reports Page
# ------------------------------------------

@dashboard_bp.route("/reports")
def reports():
    """Display reports with charts."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = report_service.get_report_data()

    return render_template(
        "reports.html",
        data=data
    )
