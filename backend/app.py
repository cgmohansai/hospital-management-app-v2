from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    # load env varaible from the .env
    load_dotenv() 
    #config
    app.config.from_object(LocalDevelopmentConfig)
    #connection for flask with flask_sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    #flask security stuf
    from flask_security import SQLAlchemyUserDatastore
    from extensions import security
    datastore = SQLAlchemyUserDatastore(db, Role, User)
    security.init_app(app, datastore = datastore, register_blueprint = False)  # we dont go into the blueprint, we run the app through the apis

    app.datastore = datastore

    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
