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
        # need checks if key is present in model (data validation check)
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
        
        db.session.delete(item)
        db.session.commit()
        return {"message": "item with {id} deleted successfully"}
    
    @staticmethod
    def update(data):
        """{'id' : 1, 'phone': 'abc'..}"""
        item = model.query.get(data["id"])
        if not item:
            raise ServiceError("not found")
        
        #preproces date if it's a string
        processed_data = data.copy()
        if 'dob' in processed_data and isinstance(processed_data['dob'], str):
            processed_data['dob'] = datetime.strptime(processed_data['dob'], '%Y-%m-%d').date()
        
        #if key is present in model
        print(item.phone)
        print(processed_data)
        for key in processed_data:
            if key != 'id':  #Don't need to update the id
                setattr(item, key, processed_data[key])
        db.session.commit()
        return item

