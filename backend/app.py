from flask import Flask
from config import LocalDevelopmentConfig
from flask_security import Security

def create_app():
    app = Flask(__name__)
    #config
    app.config.from_object(LocalDevelopmentConfig)
    #connection for flask with flask_sqlalchemy
    from models import db, User, Role
    db.init_app(app)

    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
