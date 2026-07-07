from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services.appointment_service import AppointmentService
from services.service_errors import ServiceError

                          
patient_field = {
    "id": fields.Integer,
    "phone": fields.String,
    "user": fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
        "email": fields.String,
    })
}

                         
doctor_field = {
    "id": fields.Integer,
    "specialization": fields.String,
    "user": fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
        "email": fields.String,
    }),
    "department": fields.Nested({
        "name": fields.String
    })
}

                               
marshal_fields = {
    "id": fields.Integer,
    "patient_id": fields.Integer,
    "doctor_id": fields.Integer,
    "status": fields.String,
    "date": fields.String(attribute=lambda x: x.date.isoformat() if x.date else None),
    "time": fields.String(attribute=lambda x: x.time.strftime('%H:%M:%S') if x.time else None),
    "created_at": fields.DateTime(dt_format='iso8601'),
    "updated_at": fields.DateTime(dt_format='iso8601'),
    "patient": fields.Nested(patient_field, allow_null=True),
    "doctor": fields.Nested(doctor_field, allow_null=True),
    "treatment": fields.Nested({
        "diagnosis": fields.String,
        "tests": fields.String,
        "prescription": fields.String,
        "medicines": fields.String,
        "visit_type": fields.String,
        "notes": fields.String
    }, allow_null=True)
}

parser = reqparse.RequestParser()
parser.add_argument("patient_id", type=int, required=True)
parser.add_argument("doctor_id", type=int, required=True)
parser.add_argument("status", type=str, choices=('Booked', 'Completed', 'Cancelled'), required=False)
parser.add_argument("date", type=str, required=True)
parser.add_argument("time", type=str, required=True)

"""/api/appointment/:id"""
class AppointmentResource(Resource):
    
    def get(self, id):  
        try:
            item = AppointmentService.get_by_id(id)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def put(self, id):  
        try:
            args = parser.parse_args()
            args["id"] = id
            item = AppointmentService.update(args)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def patch(self, id):
        try:
            data = request.get_json()
            data["id"] = id
            item = AppointmentService.update(data)       
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404
    
    def delete(self, id):
        try:
            item = AppointmentService.delete(id)
            return marshal(item, marshal_fields), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

"""/api/appointment -> get, post""" 
class AppointmentListResource(Resource):
    
    def get(self):
        filters = {}
        if request.args.get('patient_id'):
            filters['patient_id'] = request.args.get('patient_id')
        if request.args.get('doctor_id'):
            filters['doctor_id'] = request.args.get('doctor_id')
            
        items = AppointmentService.get_all(filters)
        return marshal(items, marshal_fields), 200
    
    def post(self):
        args = parser.parse_args()
        item = AppointmentService.create(args)
        return marshal(item, marshal_fields), 201

