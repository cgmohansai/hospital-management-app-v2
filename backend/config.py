import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_123")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "dev_salt_123")
    SECURITY_PASSWORD_HASH = "argon2"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TOKEN_AUTHENTICATION_KEY = "auth_token"
    SECURITY_TOKEN_AUTHENTICATION_REALM = "Authentication Required"

class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True

    CELERY = {
        "broker_url": "redis://localhost:6379/0",
        "result_backend": "redis://localhost:6379/0",
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