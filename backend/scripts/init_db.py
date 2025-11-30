from flask_security import hash_password
from app import app
from models import db
from flask_security import SQLAlchemyUserDatastore

# from backend
# py -m scripts.init_db 

with app.app_context():
    db.drop_all() # delete existing tables
    db.create_all() # fresh tables , refresh steps
    
    datastore : SQLAlchemyUserDatastore = app.datastore  #datastore from the app context

    admin_role = datastore.find_or_create_role("admin", description="Super User")
    doctor_role = datastore.find_or_create_role("doctor", description="Doctor User")
    patient_role = datastore.find_or_create_role("patient", description="Patient User")

    if not datastore.find_user(email = "admin@study"):
        datastore.create_user(
            username = "admin01",
            email = "admin@study",
            name = "Admin_01", 
            password = hash_password("pass")
        )

    
    if not datastore.find_user(email = "doctor@study"):
        datastore.create_user(
            username = "doctor01",
            email = "doctor@study",
            name = "doctor_01",
            password = hash_password("pass")
        )

    if not datastore.find_user(email = "patient@study"):
        datastore.create_user(
            username = "patient01",
            email = "patient@study",
            name = "patient_01",
            password = hash_password("pass")
        )

    try:    
        db.session.commit()
        print("Roles created")
    except:
        db.session.rollback()
        print("Error while creating roles")

    admin01 = datastore.find_user(email="admin@study")
    doctor01 = datastore.find_user(email="doctor@study")
    patient01 = datastore.find_user(email="patient@study")

    admin_role = datastore.find_role("admin")
    doctor_role = datastore.find_role("doctor")
    patient_role = datastore.find_role("patient")
    
    datastore.add_role_to_user(admin01, admin_role)
    datastore.add_role_to_user(doctor01, doctor_role)
    datastore.add_role_to_user(patient01, patient_role)

    try:
        db.session.commit()
        print("added roles")
    except:
        db.session.rollback()
        print("error adding roles")