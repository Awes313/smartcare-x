"""
Entry point for SmartCare X.

Local development:  flask run   (or)  python app.py
Production (Render): gunicorn app:app   (see Procfile)
"""

from smartcare import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
