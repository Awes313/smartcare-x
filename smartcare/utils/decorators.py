"""
Access-control decorators layered on top of Flask-Login's @login_required.

Usage:
    @patient_bp.route("/dashboard")
    @login_required
    @role_required("patient")
    def dashboard():
        ...
"""

from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user

from smartcare.models.user import RoleEnum


def role_required(*allowed_roles):
    """
    Restrict a view to one or more roles, e.g. @role_required("doctor", "admin").
    Must be used *below* @login_required so current_user is guaranteed to exist.
    """
    normalized = {RoleEnum(r) if not isinstance(r, RoleEnum) else r for r in allowed_roles}

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in normalized:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


def verified_email_required(view_func):
    """Blocks access until the user has confirmed their email address."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if not current_user.is_email_verified:
            flash("Please verify your email address to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapped


def active_account_required(view_func):
    """Blocks access for deactivated accounts (e.g. suspended by admin)."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated and not current_user.is_active:
            flash("Your account has been deactivated. Contact the hospital admin.", "danger")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapped
