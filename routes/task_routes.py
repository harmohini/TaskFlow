from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from services.task_service import TaskService
from services.auth_service import AuthService

task_bp = Blueprint("tasks", __name__)
task_service = TaskService()
auth_service = AuthService()


# ==========================================
# List Tasks
# ==========================================

@task_bp.route("/tasks")
def list_tasks():
    """Display all tasks with search and filters."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")

    tasks = task_service.get_all_tasks(
        search=search, status=status, priority=priority
    )
    users = auth_service.get_all_users()

    return render_template(
        "tasks.html",
        tasks=tasks,
        users=users,
        search=search,
        filter_status=status,
        filter_priority=priority
    )


# ==========================================
# Add Task
# ==========================================

@task_bp.route("/tasks/add", methods=["GET", "POST"])
@task_bp.route("/tasks/add/<int:project_id>", methods=["GET", "POST"])
def add_task(project_id=None):
    """Create a new task."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from services.project_service import ProjectService
    project_service = ProjectService()
    projects = project_service.get_all_projects()
    users = auth_service.get_all_users()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        due_date = request.form.get("due_date", "")
        assigned_to = request.form.get("assigned_to") or None
        proj_id = request.form.get("project_id", project_id)

        if not title or not proj_id:
            flash("Title and Project are required.", "danger")
            return render_template("add_task.html", projects=projects, users=users, project_id=project_id)

        result = task_service.create_task(
            proj_id, title, description, priority,
            due_date, assigned_to, session["user_id"]
        )
        flash(result["message"], "success" if result["success"] else "danger")
        return redirect(url_for("tasks.list_tasks"))

    return render_template("add_task.html", projects=projects, users=users, project_id=project_id)


# ==========================================
# Edit Task
# ==========================================

@task_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    """Edit an existing task."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    task = task_service.get_task_by_id(task_id)
    if not task:
        flash("Task not found.", "danger")
        return redirect(url_for("tasks.list_tasks"))

    from services.project_service import ProjectService
    project_service = ProjectService()
    projects = project_service.get_all_projects()
    users = auth_service.get_all_users()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        status = request.form.get("status", "To Do")
        due_date = request.form.get("due_date", "")
        assigned_to = request.form.get("assigned_to") or None

        if not title:
            flash("Title is required.", "danger")
            return render_template("edit_task.html", task=task, projects=projects, users=users)

        result = task_service.update_task(
            task_id, title, description, priority, status,
            due_date, assigned_to, session["user_id"]
        )
        flash(result["message"], "success" if result["success"] else "danger")
        return redirect(url_for("tasks.list_tasks"))

    return render_template("edit_task.html", task=task, projects=projects, users=users)


# ==========================================
# Assign Task
# ==========================================

@task_bp.route("/tasks/<int:task_id>/assign", methods=["POST"])
def assign_task(task_id):
    """Assign a task to a user."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    assigned_to = request.form.get("assigned_to") or None
    result = task_service.assign_task(task_id, assigned_to, session["user_id"])
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("tasks.list_tasks"))


# ==========================================
# Change Task Status (AJAX)
# ==========================================

@task_bp.route("/tasks/<int:task_id>/status", methods=["POST"])
def change_task_status(task_id):
    """Change task status via AJAX."""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    new_status = data.get("status", "")

    if new_status not in ["To Do", "In Progress", "Review", "Completed"]:
        return jsonify({"success": False, "message": "Invalid status."}), 400

    result = task_service.update_task_status(task_id, new_status, session["user_id"])
    return jsonify(result)


# ==========================================
# Delete Task
# ==========================================

@task_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    """Delete a task."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    result = task_service.delete_task(task_id, session["user_id"])
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("tasks.list_tasks"))