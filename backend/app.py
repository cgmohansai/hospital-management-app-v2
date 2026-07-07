import os

from flask import Flask
from flask_cors import CORS

from config import LocalDevelopmentConfig, ProductionConfig
from resources import auth_bp, api_bp, api
from celery_factory import make_celery

def create_app():
    app = Flask(__name__)
    config_name = os.getenv("FLASK_CONFIG", "development")
    config_class = ProductionConfig if config_name == "production" else LocalDevelopmentConfig

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_class)

    from models import db, User, Role
    db.init_app(app)

                        
    from flask_security import SQLAlchemyUserDatastore
    from extensions import security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore = datastore, register_blueprint = True)

    app.datastore = datastore

                
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    
    with app.app_context():
        db.create_all()
    return app

app = create_app()
celery = make_celery(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
