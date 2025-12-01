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
        
        # Delete appointments first to avoid FK constraint
        from models import Appointment
        Appointment.query.filter_by(doctor_id=id).delete()
        
        # Delete the User (which cascades to Doctor profile)
        # We need to get the user before deleting the doctor if we want to delete the user.
        # But wait, if we delete the doctor item, the user remains.
        # If we want to delete the USER, we should do that.
        user = item.user
        if user:
            db.session.delete(user)
        else:
            # Fallback if no user (shouldn't happen)
            db.session.delete(item)
            
        db.session.commit()
        return {"message": f"Doctor with {id} deleted successfully"}
    
    @staticmethod
    def update(data):
        """{'id' : 1, 'specialization': 'abc', 'name': 'New Name'..}"""
        item = model.query.get(data["id"])
        if not item:
            raise ServiceError("not found")
        
        # Separate Doctor fields and User fields
        doctor_fields = ['specialization', 'bio', 'is_active', 'department_id', 'phone']
        user_fields = ['username', 'email', 'name'] # Phone is now in Doctor model
        
        # Update Doctor fields
        for key in data:
            if key in doctor_fields and data[key] is not None:
                setattr(item, key, data[key])
        
        # Update User fields
        if item.user:
            for key in data:
                if key in user_fields and data[key] is not None:
                    setattr(item.user, key, data[key])
            
            # Handle password separately
            if 'password' in data and data['password']:
                from flask_security.utils import hash_password
                item.user.password = hash_password(data['password'])
                
            # Sync active status if is_active is updated
            if 'is_active' in data and data['is_active'] is not None:
                item.user.active = data['is_active']

        db.session.commit()
        return item

    @staticmethod
    def get_availability_slots(doctor_id, start_date=None, days=7):
        from datetime import datetime, timedelta, date, time
        from models import DoctorAvailability, Appointment

        if start_date is None:
            start_date = date.today()
        
        availability_data = []
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Get availability for this date
            # Assuming DoctorAvailability stores specific dates as per seed.py
            # If it was recurring, logic would be different (checking day of week)
            day_availability = DoctorAvailability.query.filter_by(
                doctor_id=doctor_id, 
                date=current_date
            ).first()
            
            slots = []
            if day_availability:
                # Generate slots
                current_time = datetime.combine(current_date, day_availability.start_time)
                end_time = datetime.combine(current_date, day_availability.end_time)
                slot_duration = timedelta(minutes=day_availability.slot_duration_minutes)
                
                # Get appointments for this day
                appointments = Appointment.query.filter_by(
                    doctor_id=doctor_id,
                    date=current_date
                ).filter(Appointment.status != 'Cancelled').all()
                
                booked_times = [appt.time for appt in appointments]
                
                while current_time + slot_duration <= end_time:
                    slot_start = current_time.time()
                    slot_end = (current_time + slot_duration).time()
                    
                    is_booked = False
                    # Simple check: if slot start matches an appointment time
                    # Ideally should check overlap, but assuming fixed slots for now
                    if slot_start in booked_times:
                        is_booked = True
                        
                    slots.append({
                        "start_time": slot_start.strftime("%H:%M"),
                        "end_time": slot_end.strftime("%H:%M"),
                        "is_booked": is_booked
                    })
                    
                    current_time += slot_duration
            
            availability_data.append({
                "date": current_date.isoformat(),
                "day_name": current_date.strftime("%A"),
                "slots": slots
            })
            
        return availability_data

    @staticmethod
    def set_availability(doctor_id, data):
        from models import DoctorAvailability
        from datetime import datetime
        
        # data: { 'date': 'YYYY-MM-DD', 'start_time': 'HH:MM', 'end_time': 'HH:MM' }
        
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time_obj = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time_obj = datetime.strptime(data['end_time'], '%H:%M').time()
        
        # Check if availability exists for this date
        availability = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj
        ).first()
        
        if availability:
            availability.start_time = start_time_obj
            availability.end_time = end_time_obj
        else:
            availability = DoctorAvailability(
                doctor_id=doctor_id,
                date=date_obj,
                start_time=start_time_obj,
                end_time=end_time_obj
            )
            db.session.add(availability)
            
        db.session.commit()
        return availability
