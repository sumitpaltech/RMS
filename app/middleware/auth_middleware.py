from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Decorator — protects routes that need authentication.
    Like Laravel's middleware('auth').
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def guest_only(f):
    """
    Decorator — redirect logged-in users away from guest pages (login/register).
    Like Laravel's middleware('guest').
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" in session:
            return redirect(url_for("task.index"))
        return f(*args, **kwargs)
    return decorated
