from flask_sqlalchemy import SQLAlchemy
from flask_security.core import Security

db = SQLAlchemy() # also fine if this is present in the models
security = Security() # inroder to use the data store