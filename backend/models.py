import uuid
from extensions import db
from datetime import datetime, timezone
from flask_security.core import UserMixin, RoleMixin

class BaseModel(db.Model):                                                            
    __abstract__ = True                              

    id = db.Column(db.Integer,primary_key = True)   
    created_at = db.Column(db.DateTime(timezone = True), default = lambda:datetime.now(timezone.utc), nullable = False)                                                                                       
                                                                          
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda:datetime.now(timezone.utc), 
    onupdate = lambda:datetime.now(timezone.utc), nullable = False)

class User(BaseModel, UserMixin):                                  
    __tablename__ = "users"

    username = db.Column(db.String, nullable = False, unique = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

                            
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False, default=lambda: str(uuid.uuid4()))                                                                              
    active = db.Column(db.Boolean, default = True)                                           

                      
                 
    roles = db.Relationship('Role', backref = 'users', secondary = 'user_roles', lazy = 'joined')                                                                          
               
    doctor_profile = db.Relationship('Doctor', back_populates = 'user', uselist = False, cascade = 'all, delete-orphan')                                                                                        
    patient_profile = db.Relationship('Patient', back_populates = 'user', uselist = False, cascade = 'all, delete-orphan')                                                                                  

class Role(BaseModel, RoleMixin):                               
    __tablename__ = "roles"

    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)

class UserRoles(BaseModel):                             
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

class Appointment(BaseModel):
    __tablename__ = "appointments"

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable = False, index = True)                             
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable = False, index = True)
    status = db.Column(db.Enum("Booked", "Completed", "Cancelled", name = "appointment_status"), nullable = False)
    time = db.Column(db.Time, nullable = False)
    date = db.Column(db.Date, nullable = False)

              
    patient = db.Relationship('Patient', back_populates='appointments')
    doctor = db.Relationship('Doctor', back_populates='appointments')
    
    treatment = db.Relationship('Treatment',back_populates='appointment',uselist=False, cascade = 'all, delete-orphan')

class Treatment(BaseModel):
    __tablename__ = "treatments"

    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), unique = True, nullable = False)
    diagnosis = db.Column(db.Text)
    tests = db.Column(db.Text)
    prescription = db.Column(db.Text)
    medicines = db.Column(db.Text)
    visit_type = db.Column(db.String)
    notes = db.Column(db.Text)

    appointment = db.Relationship('Appointment', back_populates = 'treatment')

class Patient(BaseModel):
    __tablename__ = "patients"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique = True, nullable = False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String)
    phone = db.Column(db.String, nullable = False)
    address = db.Column(db.String)

    user = db.Relationship('User', back_populates='patient_profile')
    appointments = db.Relationship('Appointment', back_populates='patient')

class Doctor(BaseModel):
    __tablename__ = "doctors"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique = True, nullable = False)
    specialization = db.Column(db.String, nullable=False)
    bio = db.Column(db.Text)
    qualification = db.Column(db.String)
    experience = db.Column(db.String)
    phone = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    user = db.Relationship('User', back_populates='doctor_profile')
    department = db.Relationship('Department', back_populates='doctors')

    availability_slots = db.Relationship('DoctorAvailability', back_populates='doctor', cascade='all, delete-orphan')

    appointments = db.Relationship('Appointment', back_populates='doctor')

class Department(BaseModel):
    __tablename__ = "departments"

    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    doctors = db.Relationship('Doctor', back_populates='department')

class DoctorAvailability(BaseModel):
    __tablename__ = "doctor_availability"

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    slot_duration_minutes = db.Column(db.Integer, default=30, nullable=False)

    doctor = db.Relationship('Doctor', back_populates='availability_slots')

class Request(BaseModel):
    __tablename__ = "requests"

    data = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)