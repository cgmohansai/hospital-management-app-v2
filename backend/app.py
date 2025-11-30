from flask import Flask
from config import LocalDevelopmentConfig
from resources import auth_bp, api_bp, api   #simply resources, imports from init file in resources

def create_app():
    app = Flask(__name__)
    # load env varaible from the .env from the config 
    #config
    app.config.from_object(LocalDevelopmentConfig)
    #connection for flask with flask_sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    #flask security stuf
    from flask_security import SQLAlchemyUserDatastore
    from extensions import security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore = datastore, register_blueprint = True)  # true for the working of the flask security login page. we dont go into the blueprint, we run the app through the apis

    app.datastore = datastore

    # blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    # api.init_app(app)
    # for trial 
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
