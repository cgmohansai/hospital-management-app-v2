from flask_restful import fields

department_field = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
}

user_field = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "username": fields.String,
    "active": fields.Boolean,
}

patient_field = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "dob": fields.String(attribute=lambda x: x.dob.isoformat() if x.dob else None),
    "gender": fields.String,
    "phone": fields.String,
    "address": fields.String,
    "user": fields.Nested(user_field),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
}

doctor_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "specialization": fields.String,
    "bio": fields.String,
    "is_active": fields.Boolean,
    "department_id": fields.Integer,
    "department": fields.Nested(department_field),
    "user": fields.Nested(user_field),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
}

