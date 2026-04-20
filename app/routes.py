"""
Blueprint principal — vistas HTML + API REST.
Las rutas de API delegan al MethodRegistry; las vistas usan Jinja2.
"""
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user

from app.core.method_registry import registry

main_bp = Blueprint("main", __name__)


# ─── Vistas HTML ────────────────────────────────────────────────

@main_bp.route("/")
def index():
    """Página principal: dashboard de bienvenida."""
    methods = registry.list_all()
    return render_template("index.html", methods=methods)


@main_bp.route("/solver/<method_name>")
def solver(method_name: str):
    """Página del solver para un método específico."""
    try:
        method = registry.get(method_name)
    except KeyError:
        return render_template("index.html", methods=registry.list_all(), error=f"Método '{method_name}' no encontrado."), 404
    return render_template("solver.html", method=method, methods=registry.list_all())


@main_bp.route("/history")
def history():
    """Historial de cálculos del usuario autenticado."""
    if not current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    from app.models import CalculationHistory
    calcs = (
        CalculationHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(CalculationHistory.created_at.desc())
        .limit(50)
        .all()
    )
    return render_template("history.html", calculations=calcs, methods=registry.list_all())


# ─── API REST ───────────────────────────────────────────────────

@main_bp.route("/api/methods", methods=["GET"])
def api_methods():
    """Lista todos los métodos numéricos disponibles."""
    return jsonify(registry.list_all())


@main_bp.route("/api/solve", methods=["POST"])
def api_solve():
    """Resuelve un sistema/ecuación usando el método indicado."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Body JSON requerido."}), 400

    method_name = data.get("method")
    if not method_name:
        return jsonify({"error": "Campo 'method' requerido."}), 400

    try:
        method = registry.get(method_name)
    except KeyError as e:
        return jsonify({"error": str(e)}), 400

    try:
        if method.method_type == "root":
            # Métodos de búsqueda de raíces: f(x) = 0
            expr = data.get("expr")
            params = data.get("params", {})
            if not expr:
                return jsonify({"error": "Campo 'expr' requerido para métodos de raíces."}), 400
            result = method.solve(expr, params)
        else:
            # Métodos de sistemas lineales: Ax = b
            matrix = data.get("matrix")
            b = data.get("b")
            if matrix is None or b is None:
                return jsonify({"error": "Campos 'matrix' y 'b' requeridos para sistemas lineales."}), 400
            result = method.solve(matrix, b)

        # Guardar en historial si el usuario está logueado
        if current_user.is_authenticated:
            from app.extensions import db
            from app.models import CalculationHistory

            calc = CalculationHistory(
                user_id=current_user.id,
                method_name=method.name,
                method_description=method.description,
                steps_count=len(result.get("steps", [])),
            )

            if method.method_type == "root":
                calc.set_matrix({"expr": data.get("expr"), "params": data.get("params", {})})
                calc.set_vector([])
            else:
                calc.set_matrix(data.get("matrix"))
                calc.set_vector(data.get("b"))

            calc.set_solution(result.get("solution", []))
            db.session.add(calc)
            db.session.commit()

        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@main_bp.route("/api/history", methods=["GET"])
def api_history():
    """Devuelve historial del usuario como JSON."""
    if not current_user.is_authenticated:
        return jsonify({"error": "No autenticado."}), 401

    from app.models import CalculationHistory
    calcs = (
        CalculationHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(CalculationHistory.created_at.desc())
        .limit(50)
        .all()
    )
    return jsonify([
        {
            "id": c.id,
            "method": c.method_name,
            "description": c.method_description,
            "matrix": c.get_matrix(),
            "vector": c.get_vector(),
            "solution": c.get_solution(),
            "steps_count": c.steps_count,
            "created_at": c.created_at.isoformat() if c.created_at else "",
        }
        for c in calcs
    ])


@main_bp.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"status": "ok"})
