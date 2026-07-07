from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import DoctorService
from services.service_errors import ServiceError
from .resource_utils import validate_date
from .marshal_fields import doctor_fields

parser = reqparse.RequestParser()
parser.add_argument("user_id", type=int, required=False)                                                
parser.add_argument("specialization", type=str, required=False)                                    
parser.add_argument("bio", type=str, required=False)
parser.add_argument("phone", type=str, required=False)               
parser.add_argument("is_active", type=bool, required=False)
parser.add_argument("department_id", type=int, required=False)
             
parser.add_argument("username", type=str, required=False)
parser.add_argument("email", type=str, required=False)
parser.add_argument("name", type=str, required=False)
parser.add_argument("password", type=str, required=False)
                                                                                                                          

marshal_fields = doctor_fields
service = DoctorService

"""/api/doctor/:id"""
class DoctorResource(Resource):
                                                                       
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
            item = service.update(args)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def patch(self, id):
        try:
            item = service.get_by_id(id)
            data = request.get_json()
            data["id"] = id
            item = service.update(data)       
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def delete(self, id):
        try:
            item = service.get_by_id(id)
            message = service.delete(id)
            return message, 200
        except ServiceError as e:
            return {"message": str(e)}, 404

"""/api/doctor -> get, post""" 
class DoctorListResource(Resource):
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)

    def post(self):
        args = parser.parse_args()
        item = service.create(args)
        return marshal(item, marshal_fields)

class DoctorAvailabilityResource(Resource):
    def get(self, id):
        try:
                                                                
                                                       
                                                                                                           
            
            availability = service.get_availability_slots(id)
            return jsonify(availability)
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self, id):
        try:
            data = request.get_json()
                                          
            service.set_availability(id, data)
            return {"message": "Availability updated successfully"}, 200
        except Exception as e:
            return {"message": str(e)}, 400
