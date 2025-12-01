from flask_restful import Api
from flask import Blueprint

from resources.auth_resource import auth_bp
from .appointment_resource import AppointmentResource, AppointmentListResource
from .department_resource import DepartmentListResource, DepartmentResource
from .doctor_resource import DoctorListResource, DoctorResource, DoctorAvailabilityResource
from .patient_resource import PatientListResource, PatientResource
from .user_resource import UserListResource, UserResource, approve_user

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(AppointmentListResource, "/appointment")
api.add_resource(AppointmentResource, "/appointment/<int:id>")
api.add_resource(DepartmentListResource, "/departments")
api.add_resource(DepartmentResource, "/departments/<int:id>")
api.add_resource(DoctorListResource, "/doctors")
api.add_resource(DoctorResource, "/doctors/<int:id>")
api.add_resource(DoctorAvailabilityResource, "/doctors/<int:id>/availability")
api.add_resource(PatientListResource, "/patients")
api.add_resource(PatientResource, "/patients/<int:id>")
api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/users/<int:id>")

api_bp.add_url_rule("/user/<int:id>/approve", view_func=approve_user, methods=["PATCH"]) # add role_required admin
