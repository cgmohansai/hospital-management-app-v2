from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import UserService
from services.service_errors import ServiceError
from .resource_utils import validate_date
from .marshal_fields import user_field   
from flask_security import current_user
from flask_security.decorators import roles_required

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)
parser.add_argument("email", type=str, required=True)
parser.add_argument("username", type=str, required=False)
parser.add_argument("password", type=str, required=False)

marshal_fields = user_field
service = UserService

"""/api/user/:id"""
class UserResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function
    # -> only admin
    def get(self, id):
        try:
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and current_user.id != id:
                return {'message': "not authorized"}, 401
            item = service.get_by_id(id)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    # -> admin / (doctor / patient) own data
    def put(self, id):
        try:
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and current_user.id != id:
                return {'message': "not authorized"}, 401
            item = service.get_by_id(id)
            args = parser.parse_args()
            args["id"] = id
            item = service.update(args)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def patch(self, id):
        try:
            item = service.get_by_id(id)
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and current_user.id != id:
                return {'message': "not authorized"}, 401
            data = request.get_json()
            data["id"] = id
            item = service.update(data)       
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def delete(self, id):
        try:
            if (current_user.has_role("doctor") or current_user.has_role("patient") ) and current_user.id != id:
                return {'message': "not authorized"}, 401
            message = service.delete(id)
            return message, 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    

"""/api/user -> get, post""" 
class UserListResource(Resource):
    # admin only
    @roles_required("admin")
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)

# /user/:id/approve (only admin)
@roles_required("admin")
def approve_user(id):
    try:
        user = UserService.update({"active": True, "id": id})
        return marshal(user, user_field), 200
    except ServiceError as e:
        return {"message": str(e)}, 404

