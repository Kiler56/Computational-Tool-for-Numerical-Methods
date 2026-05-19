"""
Main blueprint — HTML views + REST API.
API routes delegate to MethodRegistry; views use Jinja2.
"""
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user

from app.core.method_registry import registry

main_bp = Blueprint("main", __name__)


# ─── HTML views ─────────────────────────────────────────────────

@main_bp.route("/")
def index():
    """Home dashboard."""
    methods = registry.list_all()
    return render_template("index.html", methods=methods)


@main_bp.route("/solver/<method_name>")
def solver(method_name: str):
    """Solver page for a specific method."""
    try:
        method = registry.get(method_name)
    except KeyError:
        return render_template(
            "index.html",
            methods=registry.list_all(),
            error=f"Method '{method_name}' was not found.",
        ), 404
    return render_template("solver.html", method=method, methods=registry.list_all())


@main_bp.route("/history")
def history():
    """Authenticated user's calculation history."""
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


# ─── REST API ───────────────────────────────────────────────────

@main_bp.route("/api/methods", methods=["GET"])
def api_methods():
    """List available numerical methods."""
    return jsonify(registry.list_all())


@main_bp.route("/api/solve", methods=["POST"])
def api_solve():
    """Run the selected numerical method."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body is required."}), 400

    method_name = data.get("method")
    if not method_name:
        return jsonify({"error": "Field 'method' is required."}), 400

    try:
        method = registry.get(method_name)
    except KeyError as e:
        return jsonify({"error": str(e)}), 400

    try:
        if method.method_type == "root":
            expr = data.get("expr")
            params = data.get("params", {})
            if not expr:
                return jsonify({"error": "Field 'expr' is required for root-finding methods."}), 400
            result = method.solve(expr, params)
        elif method.method_type == "interpolation":
            # Can receive either:
            # 1. x (list of floats) and y (list of floats) with optional params (containing eval_x / x_eval)
            # 2. points (list of [x, y] lists) and x_eval
            x_points = data.get("x")
            y_points = data.get("y")
            points = data.get("points")
            x_eval = data.get("x_eval")
            params = data.get("params", {})

            if points is not None:
                if not x_points or not y_points:
                    x_points = [p[0] for p in points]
                    y_points = [p[1] for p in points]
            elif x_points is not None and y_points is not None:
                if points is None:
                    points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
            else:
                return jsonify({"error": "Fields 'x' and 'y' (or 'points') are required for interpolation."}), 400

            # Determine x_eval
            if x_eval is None and params and params.get("eval_x") is not None:
                x_eval = params["eval_x"]
            if x_eval is not None:
                x_eval = float(x_eval)

            import inspect
            sig = inspect.signature(method.solve)
            if 'points' in sig.parameters:
                result = method.solve(points, x_eval=x_eval)
            else:
                if x_eval is not None:
                    params["eval_x"] = x_eval
                if 'params' in sig.parameters:
                    result = method.solve(x_points, y_points, params=params)
                else:
                    result = method.solve(x_points, y_points)
        else:
            matrix = data.get("matrix")
            b = data.get("b")
            params = data.get("params", {})
            if matrix is None or b is None:
                return jsonify({"error": "Fields 'matrix' and 'b' are required for linear systems."}), 400
            
            import inspect
            sig = inspect.signature(method.solve)
            if 'params' in sig.parameters:
                result = method.solve(matrix, b, params=params)
            else:
                result = method.solve(matrix, b)

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
            elif method.method_type == "interpolation":
                calc.set_matrix({"x": x_points, "y": y_points, "points": points})
                calc.set_vector([x_eval] if x_eval is not None else [])
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
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@main_bp.route("/api/history", methods=["GET"])
def api_history():
    """Return the user's history as JSON."""
    if not current_user.is_authenticated:
        return jsonify({"error": "Not authenticated."}), 401

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
