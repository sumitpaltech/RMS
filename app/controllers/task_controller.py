from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.task_model import Task
from app.middleware.auth_middleware import login_required

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("/")
@login_required
def index():
    """GET /tasks — list all tasks for logged-in user"""
    # Use the email from the session because your schema uses 'assigned_to' (VARCHAR)
    user_identity = session.get("email") 
    
    tasks = Task.by_user(user_identity)
    stats = Task.count_by_status(user_identity)
    
    return render_template("tasks/index.html", tasks=tasks, stats=stats)

@task_bp.route("/store", methods=["POST"])
@login_required
def store():
    """POST /tasks/store — save new task"""
    # Collect all fields from your task_tracker schema
    data = {
        "title": request.form.get("title", "").strip(),
        "description": request.form.get("description", "").strip(),
        "category": request.form.get("category", "General"),
        "assigned_to": session.get("email"), # Mapping to your schema
        "priority": request.form.get("priority", "medium"),
        "start_date": request.form.get("start_date") or None,
        "due_date": request.form.get("due_date") or None,
        "status": request.form.get("status", "pending"),
        "remarks": request.form.get("remarks", "").strip()
    }

    if not data["title"]:
        flash("Title is required.", "danger")
        return redirect(url_for("task.create"))

    # Pass the data dictionary to the updated Task.create method
    Task.create(data)
    flash("Task created successfully!", "success")
    return redirect(url_for("task.index"))

@task_bp.route("/<int:id>", methods=["GET"])
@login_required
def show(id):
    """GET /tasks/<id> — view single task"""
    task = Task.find_with_user(id)
    # Check against assigned_to email instead of user_id
    if not task or task["assigned_to"] != session.get("email"):
        flash("Task not found.", "danger")
        return redirect(url_for("task.index"))
    return render_template("tasks/show.html", task=task)

@task_bp.route("/<int:id>/update", methods=["POST"])
@login_required
def update(id):
    """POST /tasks/<id>/update — save task changes"""
    task = Task.find(id)
    if not task or task["assigned_to"] != session.get("email"):
        flash("Task not found.", "danger")
        return redirect(url_for("task.index"))

    # Update logic matching your table columns
    title       = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    status      = request.form.get("status", "pending")
    priority    = request.form.get("priority", "medium")
    due_date    = request.form.get("due_date") or None

    if not title:
        flash("Title is required.", "danger")
        return redirect(url_for("task.edit", id=id))

    Task.update(id, title, description, status, priority, due_date)
    flash("Task updated successfully!", "success")
    return redirect(url_for("task.index"))

# app/controllers/task_controller.py

@task_bp.route("/create", methods=["GET"])
@login_required
def create():
    """GET /tasks/create — show create form"""
    return render_template("tasks/create.html")