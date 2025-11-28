class BaseConfig:
    SQL_ALCHEMY_TRRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False