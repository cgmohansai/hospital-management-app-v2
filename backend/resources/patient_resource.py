from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import PatientService
from services.service_errors import ServiceError
from .resource_utils import validate_date
from .marshal_fields import patient_field   
from flask_security import current_user

parser = reqparse.RequestParser()
parser.add_argument("user_id", type=int, required=False)
parser.add_argument("dob", type=str, required=False)
parser.add_argument("gender", type=str, required=False)
parser.add_argument("phone", type=str, required=False)
parser.add_argument("address", type=str, required=False)
# User fields
parser.add_argument("username", type=str, required=False)
parser.add_argument("email", type=str, required=False)
parser.add_argument("name", type=str, required=False)
parser.add_argument("password", type=str, required=False)
parser.add_argument("is_active", type=bool, required=False) # For blacklisting

marshal_fields = patient_field
service = PatientService

"""/api/patient/:id"""
class PatientResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function
    # -> only admin
    def get(self, id):
        try:
            item = service.get_by_id(id)
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and item.user_id != current_user.id:
                return {'message': "not authorized"}, 401
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    # -> admin / (doctor / patient) own data
    def put(self, id):
        try:
            item = service.get_by_id(id)
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and item.user_id != current_user.id:
                return {'message': "not authorized"}, 401
            args = parser.parse_args()
            args["id"] = id
            item = service.update(args)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def patch(self, id):
        try:
            item = service.get_by_id(id)
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and item.user_id != current_user.id:
                return {'message': "not authorized"}, 401
            data = request.get_json()
            data["id"] = id
            item = service.update(data)       
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def delete(self, id):
        try:
            item = service.get_by_id(id)
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and item.user_id != current_user.id:
                return {'message': "not authorized"}, 401
            message = service.delete(id)
            return message, 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    

"""/api/patient -> get, post""" 
class PatientListResource(Resource):
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)
    
    def post(self):
        args = parser.parse_args()
        item = service.create(args)
        return marshal(item, marshal_fields)

