import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.sqlite3")
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_123")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "dev_salt_123")
    SECURITY_PASSWORD_HASH = "argon2"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TOKEN_AUTHENTICATION_KEY = "auth_token"
    SECURITY_TOKEN_AUTHENTICATION_REALM = "Authentication Required"

class LocalDevelopmentConfig(BaseConfig):
    DEBUG = True

    CELERY = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        "result_backend": os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        "task_ignore_result": True,
        "beat_schedule": {
            "daily-reminder-task": {
                "task": "tasks.send_daily_reminders",
                "schedule": crontab(hour=7, minute=0),
            },
            "monthly-report-task": {
                "task": "tasks.send_monthly_reports",
                "schedule": crontab(day_of_month=1, hour=0, minute=0),
            }
        }
    }

class ProductionConfig(BaseConfig):
    DEBUG = False
    CELERY = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        "result_backend": os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        "task_ignore_result": True,
    }