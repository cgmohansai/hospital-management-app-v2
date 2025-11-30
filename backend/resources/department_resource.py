from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import DepartmentService
from services.service_errors import ServiceError
from .resource_utils import validate_date
from .marshal_fields import department_field   
from flask_security import current_user

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)
parser.add_argument("description", type=str, required=False)

marshal_fields = department_field
service = DepartmentService

"""/api/department/:id"""
class DepartmentResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function
    def get(self, id):
        try:
            item = service.get_by_id(id)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def put(self, id):
        try:
            item = service.get_by_id(id)
            args = parser.parse_args()
            args["id"] = id
            args["id"] = id
            item = service.update(args)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def patch(self, id):
        try:
            item = service.get_by_id(id)
            data = request.get_json()
            data["id"] = id
            data["id"] = id
            
            item = service.update(data)       
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def delete(self, id):
        try:
            item = service.get_by_id(id)
            item = service.get_by_id(id)
            
            message = service.delete(id)
            return message, 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    

"""/api/department -> get, post""" 
class DepartmentListResource(Resource):
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)
    
    def post(self):
        args = parser.parse_args()
        args = parser.parse_args()
        
        item = service.create(args)
        return marshal(item, marshal_fields)
        

