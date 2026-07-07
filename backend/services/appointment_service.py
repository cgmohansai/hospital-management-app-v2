from models import Appointment, db
from services.service_errors import ServiceError
from datetime import datetime

class AppointmentService:
    
    @staticmethod
    def get_all(filters=None):
        if filters:
            return Appointment.query.filter_by(**filters).all()
        return Appointment.query.all()
    
    @staticmethod
    def get_by_id(id):
        appointment = Appointment.query.get(id)
        if not appointment:
            raise ServiceError("not found")
        return appointment
    
    @staticmethod
    def create(data):
                               
        processed_data = data.copy()
        
        if 'date' in processed_data and isinstance(processed_data['date'], str):
            processed_data['date'] = datetime.strptime(processed_data['date'], '%Y-%m-%d').date()
        
        if 'time' in processed_data and isinstance(processed_data['time'], str):
                                                                    
            if len(processed_data['time'].split(':')) == 2:
                processed_data['time'] = datetime.strptime(processed_data['time'], '%H:%M').time()
            else:
                processed_data['time'] = datetime.strptime(processed_data['time'], '%H:%M:%S').time()
        
        appointment = Appointment(**processed_data)
        db.session.add(appointment)
        db.session.commit()
        return appointment

    @staticmethod
    def delete(id):
        appointment = Appointment.query.get(id)
        if not appointment:
            raise ServiceError("not found")
        
        db.session.delete(appointment)
        db.session.commit()
        return appointment
    
    @staticmethod
    def update(data):
        """{'id' : 1, 'patient_id': 1, 'status': 'Completed'..}"""
        appointment = Appointment.query.get(data["id"])
        if not appointment:
            raise ServiceError("not found")
        
                                                
                                                      
        processed_data = data.copy()
        
        if 'date' in processed_data and isinstance(processed_data['date'], str):
            processed_data['date'] = datetime.strptime(processed_data['date'], '%Y-%m-%d').date()
        
        if 'time' in processed_data and isinstance(processed_data['time'], str):
                                                                    
            if len(processed_data['time'].split(':')) == 2:
                processed_data['time'] = datetime.strptime(processed_data['time'], '%H:%M').time()
            else:
                processed_data['time'] = datetime.strptime(processed_data['time'], '%H:%M:%S').time()
        
                                      
        if 'treatment' in processed_data:
            treatment_data = processed_data.pop('treatment')
            from models import Treatment
            
            if appointment.treatment:
                                           
                for key, value in treatment_data.items():
                    setattr(appointment.treatment, key, value)
            else:
                                      
                treatment_data['appointment_id'] = appointment.id
                new_treatment = Treatment(**treatment_data)
                db.session.add(new_treatment)

        for key in processed_data:
            if key != 'id':                       
                setattr(appointment, key, processed_data[key])
        
        db.session.commit()
        return appointment
    

