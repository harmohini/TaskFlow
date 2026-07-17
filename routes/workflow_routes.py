from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from services.workflow_service import WorkflowService

workflow_bp = Blueprint("workflow", __name__)
workflow_service = WorkflowService()


# ==========================================
# Workflow Board
# ==========================================

@workflow_bp.route("/workflow")
def kanban_board():
    """Display the Workflow board."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    todo_tasks = workflow_service.get_tasks_by_stage("To Do")
    in_progress_tasks = workflow_service.get_tasks_by_stage("In Progress")
    review_tasks = workflow_service.get_tasks_by_stage("Review")
    completed_tasks = workflow_service.get_tasks_by_stage("Completed")

    return render_template(
        "workflow.html",
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        review_tasks=review_tasks,
        completed_tasks=completed_tasks
    )


# ==========================================
# Move Task (AJAX)
# ==========================================

@workflow_bp.route("/workflow/move", methods=["POST"])
def move_task():
    """Move a task to a new stage via AJAX."""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    task_id = data.get("task_id")
    new_stage = data.get("new_stage")

    if not task_id or not new_stage:
        return jsonify({"success": False, "message": "Missing data."}), 400

    result = workflow_service.move_task(task_id, new_stage, session["user_id"])
    return jsonify(result)


# ==========================================
# Workflow History
# ==========================================

@workflow_bp.route("/workflow/history/<int:task_id>")
def workflow_history(task_id):
    """View workflow history for a task."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    history = workflow_service.get_workflow_history(task_id)

    from services.task_service import TaskService
    task_service = TaskService()
    task = task_service.get_task_by_id(task_id)

    return render_template(
        "workflow_history.html",
        history=history,
        task=task
    )


# ==========================================
# API: Get Workflow Data (AJAX)
# ==========================================

@workflow_bp.route("/api/workflow/data")
def api_workflow_data():
    """Return workflow data as JSON for dynamic updates."""
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    todo = workflow_service.get_tasks_by_stage("To Do")
    in_progress = workflow_service.get_tasks_by_stage("In Progress")
    review = workflow_service.get_tasks_by_stage("Review")
    completed = workflow_service.get_tasks_by_stage("Completed")

    return jsonify({
        "todo": [dict(t) for t in todo],
        "in_progress": [dict(t) for t in in_progress],
        "review": [dict(t) for t in review],
        "completed": [dict(t) for t in completed]
    })