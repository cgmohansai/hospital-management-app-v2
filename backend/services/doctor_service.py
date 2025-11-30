from models import db, Doctor
from services.service_errors import ServiceError

model = Doctor

class DoctorService():
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
        item = model(**data)
        
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
        """{'id' : 1, 'specialization': 'abc'..}"""
        item = model.query.get(data["id"])
        if not item:
            raise ServiceError("not found")
        
        # need checks if key is present in model
        print(item.specialization)
        print(data)
        for key in data:
            setattr(item, key, data[key])
        db.session.commit()
        return item

