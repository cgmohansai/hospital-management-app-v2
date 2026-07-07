from models import Request, db
from services.service_errors import ServiceError

model = Request

class RequestService():
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
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return item

    @staticmethod
    def delete(id):
        item = model.query.get(id)
        if not item:
            raise ServiceError("not found")
        db.session.delete(item)
        db.session.commit()
        return {"message": "deleted", "id": id}
    
    @staticmethod
    def update(data):
        """{'id' : 1, 'status': 'approved'..}"""
        item = model.query.get(data["id"])
        if not item:
            raise ServiceError("not found")
        
                                                
        print(item.status)
        print(data)
        for key in data:
            setattr(item, key, data[key])
        
        db.session.commit()
        return item

