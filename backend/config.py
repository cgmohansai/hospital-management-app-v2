import os

class BaseConfig:
    SQL_ALCHEMY_TRRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECRET_PASSWORD_SALT = os.environ.get("SECRET_PASSWORD_SALT")

class ProductionConfig(BaseConfig):
    DEBUG = False