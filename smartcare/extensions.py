"""
Central place to instantiate Flask extensions without binding them to an
app yet. Each extension is initialized (app.init_app(app)) inside
create_app(), which avoids circular imports between blueprints/models
and the app factory.
"""

from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

# Sensible Flask-Login defaults; the actual endpoint name is set once the
# auth blueprint is registered (see smartcare/__init__.py).
login_manager.login_message_category = "warning"
