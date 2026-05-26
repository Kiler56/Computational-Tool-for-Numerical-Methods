"""
Main blueprint — HTML views + REST API.
API routes delegate to MethodRegistry; views use Jinja2.
"""
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user

from app.core.method_registry import registry
from app.core.safe_eval import make_function          # ← NUEVO
from app.core.universal_plotter import UniversalPlotter  # ← NUEVO

main_bp = Blueprint("main", __name__)


# ─── HTML views ─────────────────────────────────────────────────

@main_bp.route("/")
def index():
    methods = registry.list_all()
    return render_template("index.html", methods=methods)


@main_bp.route("/plotter")
def plotter():
    return render_template("plotter.html", methods=registry.list_all())


@main_bp.route("/solver/<method_name>")
def solver(method_name: str):
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
    return jsonify(registry.list_all())


# ── Helper ────────────────────────────────────────────────────────────────────

def _attach_plot(result: dict, expr: str | None) -> dict:
    """
    Agrega la gráfica al result como imagen base64 PNG.
    Si el plot falla (datos insuficientes, etc.) simplemente no agrega nada.
    """
    print("DEBUG: _attach_plot called, expr=", expr, "plot_type=", result.get("plot_type"))
    try:
        import io, base64
        import matplotlib
        matplotlib.use("Agg")  # sin GUI, obligatorio en servidor

        f = make_function(expr) if expr else None
        fig = UniversalPlotter(result, f=f).plot()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
        buf.seek(0)
        result["plot"] = base64.b64encode(buf.read()).decode("utf-8")

        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:
        pass   # la gráfica es opcional — nunca rompe el endpoint

    return result


# ── Endpoint principal ────────────────────────────────────────────────────────

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

    result = {}
    error_msg = None
    status_code = 200
    expr = None

    try:
        if method.method_type == "root":
            expr = data.get("expr")
            params = data.get("params", {})
            if not expr:
                raise ValueError("Field 'expr' is required for root-finding methods.")
            result = method.solve(expr, params)

        elif method.method_type == "interpolation":
            x_points = data.get("x")
            y_points = data.get("y")
            points   = data.get("points")
            x_eval   = data.get("x_eval")
            params   = data.get("params", {})

            if points is not None:
                if not x_points or not y_points:
                    x_points = [p[0] for p in points]
                    y_points = [p[1] for p in points]
            elif x_points is not None and y_points is not None:
                if points is None:
                    points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
            else:
                raise ValueError("Fields 'x' and 'y' (or 'points') are required for interpolation.")

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

        else:  # linear_system
            matrix = data.get("matrix")
            b      = data.get("b")
            params = data.get("params", {})
            if matrix is None:
                raise ValueError("Field 'matrix' is required for linear systems.")
            if b is None:
                if method.requires_vector_b:
                    raise ValueError("Field 'b' is required for this method.")
                b = [0.0] * len(matrix)

            import inspect
            sig = inspect.signature(method.solve)
            if 'params' in sig.parameters:
                result = method.solve(matrix, b, params=params)
            else:
                result = method.solve(matrix, b)

        result = _attach_plot(result, expr)

    except ValueError as e:
        error_msg = str(e)
        status_code = 400
    except ZeroDivisionError:
        error_msg = "División por cero detectada durante el cálculo. Verifique sus datos de entrada."
        status_code = 400
    except OverflowError:
        error_msg = "Desbordamiento numérico (Overflow). Los valores son demasiado grandes."
        status_code = 400
    except Exception as e:
        if "LinAlgError" in type(e).__name__:
            error_msg = f"Error de álgebra lineal: {str(e)}"
            status_code = 400
        else:
            error_msg = f"Internal error: {str(e)}"
            status_code = 500

    # --- GUARDAR HISTORIAL SIEMPRE (incluso con errores) ---
    if current_user.is_authenticated:
        from app.extensions import db
        from app.models import CalculationHistory

        calc = CalculationHistory(
            user_id=current_user.id,
            method_name=method.name,
            method_description=method.description,
            steps_count=len(result.get("steps", [])) if result else 0,
        )

        if method.method_type == "root":
            calc.set_matrix({"expr": data.get("expr"), "params": data.get("params", {})})
            calc.set_vector([])
        elif method.method_type == "interpolation":
            calc.set_matrix({"x": data.get("x") or [p[0] for p in data.get("points", [])] if data.get("points") else [], 
                             "y": data.get("y") or [p[1] for p in data.get("points", [])] if data.get("points") else [], 
                             "points": data.get("points")})
            calc.set_vector([data.get("x_eval")] if data.get("x_eval") is not None else [])
        else:
            calc.set_matrix(data.get("matrix"))
            calc.set_vector(data.get("b"))

        if error_msg:
            calc.set_solution([f"ERROR: {error_msg}"])
        else:
            calc.set_solution(result.get("solution", []))
            
        db.session.add(calc)
        db.session.commit()

    if error_msg:
        return jsonify({"error": error_msg}), status_code

    return jsonify(result)

@main_bp.route("/api/history", methods=["GET"])
def api_history():
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
