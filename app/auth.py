"""
Blueprint de autenticación — register, login, logout, profile.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.core.method_registry import registry
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


# ─── Registro ────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # Validaciones
        error = None
        if not username or not email or not password:
            error = "Todos los campos son obligatorios."
        elif len(password) < 4:
            error = "La contraseña debe tener al menos 4 caracteres."
        elif password != confirm:
            error = "Las contraseñas no coinciden."
        elif User.query.filter_by(email=email).first():
            error = "Ya existe una cuenta con ese email."
        elif User.query.filter_by(username=username).first():
            error = "Ese nombre de usuario ya está en uso."

        if error:
            return render_template(
                "auth/register.html",
                error=error,
                username=username,
                email=email,
                methods=registry.list_all(),
            )

        user = User(username=username, email=email, display_name=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("auth/register.html", methods=registry.list_all())


# ─── Login ───────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return render_template(
                "auth/login.html",
                error="Credenciales incorrectas.",
                email=email,
                methods=registry.list_all(),
            )

        login_user(user, remember=True)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.index"))

    return render_template("auth/login.html", methods=registry.list_all())


# ─── Logout ──────────────────────────────────────────────────────

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# ─── Perfil ──────────────────────────────────────────────────────

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        preferred_lang = request.form.get("preferred_lang", "es")

        if display_name:
            current_user.display_name = display_name
        if preferred_lang in ("es", "en"):
            current_user.preferred_lang = preferred_lang

        db.session.commit()
        return render_template(
            "auth/profile.html",
            success="Perfil actualizado correctamente.",
            methods=registry.list_all(),
        )

    return render_template("auth/profile.html", methods=registry.list_all())
