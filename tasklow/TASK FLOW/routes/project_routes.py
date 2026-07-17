from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from services.project_service import ProjectService
from services.auth_service import AuthService

project_bp = Blueprint("projects", __name__)
project_service = ProjectService()
auth_service = AuthService()


# ==========================================
# List Projects
# ==========================================

@project_bp.route("/projects")
def list_projects():
    """Display all projects with search and filter."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    projects = project_service.get_all_projects(search=search, status=status)

    # Get stats for each project
    project_stats = {}
    for p in projects:
        stats = project_service.get_project_stats(p["id"])
        project_stats[p["id"]] = stats

    return render_template(
        "projects.html",
        projects=projects,
        project_stats=project_stats,
        search=search,
        filter_status=status
    )


# ==========================================
# View Project Details
# ==========================================

@project_bp.route("/projects/<int:project_id>")
def project_details(project_id):
    """View a single project with its tasks."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    project = project_service.get_project_by_id(project_id)
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for("projects.list_projects"))

    stats = project_service.get_project_stats(project_id)
    users = auth_service.get_all_users()
    project_members = project_service.get_project_members(project_id)

    from services.task_service import TaskService
    task_service = TaskService()
    tasks = task_service.get_tasks_by_project(project_id)

    return render_template(
        "project_details.html",
        project=project,
        stats=stats,
        tasks=tasks,
        users=users,
        project_members=project_members
    )


# ==========================================
# Add Project
# ==========================================

@project_bp.route("/projects/add", methods=["GET", "POST"])
def add_project():
    """Create a new project with optional team members."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    users = auth_service.get_all_users()

    if request.method == "POST":
        project_name = request.form.get("project_name", "").strip()
        description = request.form.get("description", "").strip()
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")
        status = request.form.get("status", "Active")
        member_ids = request.form.getlist("members")

        if not project_name:
            flash("Project name is required.", "danger")
            return render_template("add_project.html", users=users)

        result = project_service.create_project(
            project_name, description, start_date, end_date,
            status, session["user_id"], member_ids=member_ids
        )
        flash(result["message"], "success" if result["success"] else "danger")
        return redirect(url_for("projects.list_projects"))

    return render_template("add_project.html", users=users)


# ==========================================
# Edit Project
# ==========================================

@project_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    """Edit an existing project."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    project = project_service.get_project_by_id(project_id)
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for("projects.list_projects"))

    if request.method == "POST":
        project_name = request.form.get("project_name", "").strip()
        description = request.form.get("description", "").strip()
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")
        status = request.form.get("status", "Active")

        if not project_name:
            flash("Project name is required.", "danger")
            return render_template("edit_project.html", project=project)

        result = project_service.update_project(
            project_id, project_name, description, start_date,
            end_date, status, session["user_id"]
        )
        flash(result["message"], "success" if result["success"] else "danger")
        return redirect(url_for("projects.list_projects"))

    return render_template("edit_project.html", project=project)


# ==========================================
# Delete Project
# ==========================================

@project_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    """Delete a project."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    result = project_service.delete_project(project_id, session["user_id"])
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("projects.list_projects"))


# ==========================================
# Manage Members Page
# ==========================================

@project_bp.route("/projects/<int:project_id>/members", methods=["GET", "POST"])
def manage_members(project_id):
    """Manage project team members."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    project = project_service.get_project_by_id(project_id)
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for("projects.list_projects"))

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "add":
            user_id = request.form.get("user_id")
            role = request.form.get("role", "Member")
            if user_id:
                project_service.add_member(project_id, int(user_id), role)
                project_service._log_activity(
                    session["user_id"],
                    f"Added member to project '{project['project_name']}'"
                )
                flash("Member added successfully.", "success")

        elif action == "remove":
            user_id = request.form.get("user_id")
            if user_id and int(user_id) != session["user_id"]:
                project_service.remove_member(project_id, int(user_id), session["user_id"])
                flash("Member removed successfully.", "success")
            elif user_id and int(user_id) == session["user_id"]:
                flash("You cannot remove yourself.", "danger")

        elif action == "update_role":
            user_id = request.form.get("user_id")
            role = request.form.get("role", "Member")
            if user_id:
                project_service.update_member_role(project_id, int(user_id), role, session["user_id"])
                flash("Member role updated.", "success")

        return redirect(url_for("projects.manage_members", project_id=project_id))

    members = project_service.get_project_members(project_id)
    non_members = project_service.get_non_members(project_id)

    return render_template(
        "manage_members.html",
        project=project,
        members=members,
        non_members=non_members
    )
