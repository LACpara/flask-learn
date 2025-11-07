from flask import Blueprint, flash, redirect, request, url_for, render_template
from flask_login import login_required, login_user, logout_user
from sqlalchemy import select
from ..models import User
from ..extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Invalid input.")
            return redirect(url_for("auth.login"))
        user = db.session.scalar(select(User).filter_by(username=username))
        if user is not None and user.validate_password(password):
            login_user(user)
            flash("Login success.")
            return redirect(url_for("main.index"))
        flash("Invalid username or password.")
        return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Goodbye.")
    return redirect(url_for("main.index"))
