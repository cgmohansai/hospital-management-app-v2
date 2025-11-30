from flask_restful import Api
from flask import Blueprint

from resources.auth_resource import auth_bp
from .appointment_resource import AppointmentResource, AppointmentListResource

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(AppointmentListResource, "/appointment")
api.add_resource(AppointmentResource, "/appointment/<int:id>")
