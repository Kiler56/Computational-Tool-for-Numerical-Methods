"""
Application entry point.
- Gunicorn (production): imports `app` directly via wsgi_app config.
- Development: `python run.py` runs Flask dev server.
"""
import os

from app import create_app

config_name = "prod" if os.environ.get("FLASK_ENV") == "production" else "dev"
app = create_app(config_name)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
