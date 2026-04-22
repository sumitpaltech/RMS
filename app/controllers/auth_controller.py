from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User
from app.middleware import login_required, guest_only

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
@guest_only
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.find_by_email(email)
        if user and User.verify_password(user["password"], password):
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            session["email"]     = user["email"]
            flash("Welcome back, " + user["name"] + "!", "success")
            return redirect(url_for("task.index"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
@guest_only
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if User.find_by_email(email):
            flash("Email already registered.", "danger")
            return render_template("auth/register.html")

        user_id = User.create(name, email, password)
        session["user_id"]   = user_id
        session["user_name"] = name
        
        flash("Account created successfully!", "success")
        return redirect(url_for("task.index"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
