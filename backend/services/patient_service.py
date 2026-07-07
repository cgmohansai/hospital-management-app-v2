from models import db, Patient
from services.service_errors import ServiceError
from datetime import datetime

model = Patient

class PatientService():
    @staticmethod
    def get_all():
        return model.query.all()
    
    @staticmethod
    def get_by_id(id):
        item = model.query.get(id)
        if not item:
            raise ServiceError("not found")
        return item
    
    @staticmethod
    def create(data):
                                                                        
        processed_data = data.copy()
        
        if 'dob' in processed_data and isinstance(processed_data['dob'], str):
            processed_data['dob'] = datetime.strptime(processed_data['dob'], '%Y-%m-%d').date()
        
        item = model(**processed_data)
        
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def delete(id):
        item = model.query.get(id)
        if not item:
            raise ServiceError("not found")
        
                                   
        from models import Appointment
        Appointment.query.filter_by(patient_id=id).delete()
        
                                           
        user = item.user
        if user:
            db.session.delete(user)
        else:
            db.session.delete(item)
            
        db.session.commit()
        return {"message": f"Patient with {id} deleted successfully"}
    
    @staticmethod
    def update(data):
        """{'id' : 1, 'phone': 'abc'..}"""
        item = model.query.get(data["id"])
        if not item:
            raise ServiceError("not found")
        
                         
        processed_data = data.copy()
        if 'dob' in processed_data and isinstance(processed_data['dob'], str):
            processed_data['dob'] = datetime.strptime(processed_data['dob'], '%Y-%m-%d').date()
        
        patient_fields = ['dob', 'gender', 'phone', 'address']
        user_fields = ['username', 'email', 'name']
        
                               
        for key in processed_data:
            if key in patient_fields and processed_data[key] is not None:
                setattr(item, key, processed_data[key])
                
                            
        if item.user:
            for key in processed_data:
                if key in user_fields and processed_data[key] is not None:
                    setattr(item.user, key, processed_data[key])
            
            if 'password' in processed_data and processed_data['password']:
                from flask_security.utils import hash_password
                item.user.password = hash_password(processed_data['password'])

            if 'is_active' in processed_data and processed_data['is_active'] is not None:
                item.user.active = processed_data['is_active']

        db.session.commit()
        return item

