from flask_sqlalchemy import SQLAlchemy
from flask_security.core import Security
from flask_restful import Api

db = SQLAlchemy()                                             
security = Security()                                
api = Api()                    