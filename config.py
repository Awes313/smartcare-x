"""
Application configuration.

Config is split by environment so the same codebase runs unmodified in
development (SQLite) and production (PostgreSQL on Render). The active
config class is selected in smartcare/__init__.py via create_app(config_name).
"""

import os
from datetime import timedelta

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _bool_env(key, default=False):
    value = os.environ.get(key)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


class BaseConfig:
    """Shared settings across all environments."""

    @classmethod
    def validate(cls):
        """Override in subclasses that need to enforce required env vars
        (see ProductionConfig). No-op by default."""
        pass

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-replace-me")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Uploads ---
    _upload_folder_raw = os.environ.get("UPLOAD_FOLDER", os.path.join("smartcare", "static", "uploads"))
    UPLOAD_FOLDER = (
        _upload_folder_raw if os.path.isabs(_upload_folder_raw) else os.path.join(BASE_DIR, _upload_folder_raw)
    )
    PROFILE_PHOTO_SUBDIR = "profile_photos"
    LAB_REPORT_SUBDIR = "lab_reports"
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", 5)) * 1024 * 1024

    # --- Mail ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = _bool_env("MAIL_USE_TLS", True)
    MAIL_USE_SSL = _bool_env("MAIL_USE_SSL", False)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "SmartCare X <no-reply@smartcarex.local>")

    # --- Payments (Razorpay test/sandbox) ---
    RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")
    RAZORPAY_CURRENCY = "INR"

    # --- App-level settings ---
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 10))
    PASSWORD_RESET_TOKEN_TTL = timedelta(hours=1)
    EMAIL_VERIFICATION_TOKEN_TTL = timedelta(hours=24)

    # --- Session / cookies ---
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_DURATION = timedelta(days=14)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'smartcare.db')}"
    SESSION_COOKIE_SECURE = False


def _normalize_db_url(raw_url):
    """Render (and some other hosts) hand out postgres:// URLs, but
    SQLAlchemy 1.4+/2.x requires the postgresql:// scheme."""
    if raw_url and raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql://", 1)
    return raw_url


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL"))
    SESSION_COOKIE_SECURE = True

    @classmethod
    def validate(cls):
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError(
                "DATABASE_URL environment variable must be set in production."
            )
        # Prevents accidentally deploying with the insecure default
        # SECRET_KEY (used to sign session cookies and password-reset/
        # email-verification tokens) — if this leaked or stayed as the
        # well-known default, anyone could forge those tokens.
        if not cls.SECRET_KEY or cls.SECRET_KEY == "dev-insecure-key-replace-me":
            raise RuntimeError(
                "SECRET_KEY environment variable must be set to a strong, unique value in production."
            )


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}