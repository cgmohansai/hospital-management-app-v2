                    

import uuid
import random
from datetime import datetime, timedelta, time, date

from faker import Faker
from faker_food import FoodProvider

from app import app
from models import (
    db,
    User,
    Role,
    Patient,
    Doctor,
    Appointment,
    Treatment,
    Department,
    DoctorAvailability,
)

from flask_security.utils import hash_password

fake = Faker()
fake.add_provider(FoodProvider)

def get_or_create_role(name: str, description: str = "") -> Role:
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.commit()
    return role

def create_user(username: str, name: str, email: str, password: str, roles) -> User:
    user = User.query.filter_by(email=email).first()
    if user:
        return user

    user = User(
        username=username,
        name=name,
        email=email,
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        active=True,
    )
    user.roles = roles
    db.session.add(user)
    db.session.commit()
    return user

def random_date_in_range(days_back: int = 90) -> date:
    return (datetime.utcnow() - timedelta(days=random.randint(0, days_back))).date()

def random_time_between(start_hour=9, end_hour=18) -> time:
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.choice([0, 15, 30, 45])
    return time(hour=hour, minute=minute)

def seed():
                   
    admin_role = get_or_create_role("admin", "Full access")
    doctor_role = get_or_create_role("doctor", "Registered medical professional")
    patient_role = get_or_create_role("patient", "Registered patient")
    
                          
    manager_role = Role.query.filter_by(name="manager").first()
    if manager_role:
        db.session.delete(manager_role)
        db.session.commit()

                        
    create_user(
        username="admin",
        name="Admin User",
        email="admin@study",
        password="pass",
        roles=[admin_role],
    )

                         
    dept_names = [
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "Oncology",
        "Gynecology",
        "Pediatrics",
        "General Surgery",
        "General Medicine"
    ]
    departments = []
    for name in dept_names:
        dept = Department.query.filter_by(name=name).first()
        if not dept:
            description = f"{name} Department"
            if name == "General Medicine":
                description = "Comprehensive medical care for adults, covering diagnosis, treatment, and prevention of disease."
            
            dept = Department(name=name, description=description)
            db.session.add(dept)
        departments.append(dept)
    db.session.commit()

                                    
    doctors = []
    
                         
    doctor_data = [
                    
        {
            "name": "Dr. Sarah Smith",
            "username": "sarah.smith",
            "email": "sarah.smith@lifesync.com",
            "dept": "Cardiology",
            "specialization": "Interventional Cardiologist",
            "qualification": "MBBS, MD (Medicine), DM (Cardiology)",
            "experience": "15+ Years",
            "bio": "Dr. Sarah Smith is a renowned Interventional Cardiologist with over 15 years of experience. She specializes in complex angioplasties and structural heart interventions. She is dedicated to providing patient-centric care with the latest cardiac technologies."
        },
        {
            "name": "Dr. James Wilson",
            "username": "james.wilson",
            "email": "james.wilson@lifesync.com",
            "dept": "Cardiology",
            "specialization": "Pediatric Cardiologist",
            "qualification": "MBBS, MD (Pediatrics), FACC",
            "experience": "12+ Years",
            "bio": "Dr. James Wilson is an expert in diagnosing and treating heart conditions in children. With a compassionate approach, he manages congenital heart defects and arrhythmias in pediatric patients."
        },
                   
        {
            "name": "Dr. Emily Chen",
            "username": "emily.chen",
            "email": "emily.chen@lifesync.com",
            "dept": "Neurology",
            "specialization": "Neurologist (Stroke Specialist)",
            "qualification": "MBBS, MD (Neurology), PhD",
            "experience": "18+ Years",
            "bio": "Dr. Emily Chen is a leading Neurologist specializing in stroke management and neuro-rehabilitation. She has published numerous papers on acute stroke care and is committed to improving stroke outcomes."
        },
        {
            "name": "Dr. Michael Brown",
            "username": "michael.brown",
            "email": "michael.brown@lifesync.com",
            "dept": "Neurology",
            "specialization": "Neurologist (Epilepsy)",
            "qualification": "MBBS, DNB (Neurology)",
            "experience": "10+ Years",
            "bio": "Dr. Michael Brown focuses on the comprehensive management of epilepsy and seizure disorders. He employs advanced diagnostic techniques to tailor treatment plans for his patients."
        },
                     
        {
            "name": "Dr. Robert Taylor",
            "username": "robert.taylor",
            "email": "robert.taylor@lifesync.com",
            "dept": "Orthopedics",
            "specialization": "Orthopedic Surgeon (Joint Replacement)",
            "qualification": "MBBS, MS (Orthopedics), FRCS",
            "experience": "20+ Years",
            "bio": "Dr. Robert Taylor is a senior Orthopedic Surgeon known for his expertise in hip and knee replacement surgeries. He uses minimally invasive techniques to ensure faster recovery for his patients."
        },
        {
            "name": "Dr. Lisa Davis",
            "username": "lisa.davis",
            "email": "lisa.davis@lifesync.com",
            "dept": "Orthopedics",
            "specialization": "Sports Medicine Specialist",
            "qualification": "MBBS, Diploma in Sports Medicine",
            "experience": "8+ Years",
            "bio": "Dr. Lisa Davis specializes in treating sports-related injuries. She works closely with athletes to provide rehabilitation and injury prevention strategies."
        },
                  
        {
            "name": "Dr. David Miller",
            "username": "david.miller",
            "email": "david.miller@lifesync.com",
            "dept": "Oncology",
            "specialization": "Medical Oncologist",
            "qualification": "MBBS, MD (Internal Medicine), DM (Oncology)",
            "experience": "14+ Years",
            "bio": "Dr. David Miller is a dedicated Medical Oncologist with expertise in chemotherapy and immunotherapy. He believes in a holistic approach to cancer care, addressing both physical and emotional needs."
        },
        {
            "name": "Dr. Jennifer Wilson",
            "username": "jennifer.wilson",
            "email": "jennifer.wilson@lifesync.com",
            "dept": "Oncology",
            "specialization": "Surgical Oncologist",
            "qualification": "MBBS, MS (Surgery), MCh (Surgical Oncology)",
            "experience": "16+ Years",
            "bio": "Dr. Jennifer Wilson is a skilled Surgical Oncologist specializing in the surgical management of solid tumors. She is known for her precision and patient-focused care."
        },
                    
        {
            "name": "Dr. Maria Garcia",
            "username": "maria.garcia",
            "email": "maria.garcia@lifesync.com",
            "dept": "Gynecology",
            "specialization": "Gynecologist & Obstetrician",
            "qualification": "MBBS, MD (OBG)",
            "experience": "11+ Years",
            "bio": "Dr. Maria Garcia provides comprehensive care for women's health, from adolescence to menopause. She specializes in high-risk pregnancies and minimally invasive gynecological surgeries."
        },
        {
            "name": "Dr. Susan Clark",
            "username": "susan.clark",
            "email": "susan.clark@lifesync.com",
            "dept": "Gynecology",
            "specialization": "Fertility Specialist",
            "qualification": "MBBS, DGO, Fellowship in Reproductive Medicine",
            "experience": "9+ Years",
            "bio": "Dr. Susan Clark is an expert in reproductive medicine, helping couples achieve their dream of parenthood. She offers personalized fertility treatments and counseling."
        },
                    
        {
            "name": "Dr. Thomas Anderson",
            "username": "thomas.anderson",
            "email": "thomas.anderson@lifesync.com",
            "dept": "Pediatrics",
            "specialization": "Pediatrician",
            "qualification": "MBBS, MD (Pediatrics)",
            "experience": "13+ Years",
            "bio": "Dr. Thomas Anderson is a friendly and experienced Pediatrician. He provides preventive health care for healthy children and medical care for children who are acutely or chronically ill."
        },
        {
            "name": "Dr. Karen Martinez",
            "username": "karen.martinez",
            "email": "karen.martinez@lifesync.com",
            "dept": "Pediatrics",
            "specialization": "Neonatologist",
            "qualification": "MBBS, MD (Pediatrics), DM (Neonatology)",
            "experience": "10+ Years",
            "bio": "Dr. Karen Martinez specializes in the care of newborn infants, especially the ill or premature. She is dedicated to providing the best start in life for her tiny patients."
        },
                         
        {
            "name": "Dr. William Hernandez",
            "username": "william.hernandez",
            "email": "william.hernandez@lifesync.com",
            "dept": "General Surgery",
            "specialization": "General Surgeon",
            "qualification": "MBBS, MS (General Surgery)",
            "experience": "22+ Years",
            "bio": "Dr. William Hernandez is a veteran General Surgeon with vast experience in abdominal surgeries, hernia repairs, and trauma care. He is known for his surgical precision and calm demeanor."
        },
        {
            "name": "Dr. Nancy White",
            "username": "nancy.white",
            "email": "nancy.white@lifesync.com",
            "dept": "General Surgery",
            "specialization": "Laparoscopic Surgeon",
            "qualification": "MBBS, MS (Surgery), FMAS",
            "experience": "12+ Years",
            "bio": "Dr. Nancy White specializes in advanced laparoscopic procedures. She focuses on minimally invasive techniques to reduce recovery time and post-operative pain."
        },
                          
        {
            "name": "Dr. Joseph Lee",
            "username": "joseph.lee",
            "email": "joseph.lee@lifesync.com",
            "dept": "General Medicine",
            "specialization": "General Physician",
            "qualification": "MBBS, MD (General Medicine)",
            "experience": "19+ Years",
            "bio": "Dr. Joseph Lee is a highly respected General Physician. He is an expert in managing chronic diseases like diabetes, hypertension, and infectious diseases."
        },
        {
            "name": "Dr. Patricia Walker",
            "username": "patricia.walker",
            "email": "patricia.walker@lifesync.com",
            "dept": "General Medicine",
            "specialization": "Consultant Physician",
            "qualification": "MBBS, DNB (Internal Medicine)",
            "experience": "14+ Years",
            "bio": "Dr. Patricia Walker provides comprehensive medical care for adult patients. She emphasizes preventive medicine and lifestyle modifications for better health outcomes."
        }
    ]

    for doc_data in doctor_data:
                         
        dept = Department.query.filter_by(name=doc_data["dept"]).first()
        if not dept:
            continue

        user = create_user(
            username=doc_data["username"],
            name=doc_data["name"],
            email=doc_data["email"],
            password="pass",
            roles=[doctor_role],
        )

        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if not doctor:
            doctor = Doctor(
                user_id=user.id,
                specialization=doc_data["specialization"],
                bio=doc_data["bio"],
                qualification=doc_data["qualification"],
                experience=doc_data["experience"],
                is_active=True,
                department=dept,
            )
            db.session.add(doctor)
        doctors.append(doctor)

    db.session.commit()

                           
    patients = []
    for i in range(50):
        full_name = fake.name()
        email = f"patient{i+1}@study"
        username = f"patient{i+1}"

        user = create_user(
            username=username,
            name=full_name,
            email=email,
            password="pass",
            roles=[patient_role],
        )

        patient = Patient.query.filter_by(user_id=user.id).first()
        if not patient:
            patient = Patient(
                user_id=user.id,
                dob=fake.date_between(start_date="-70y", end_date="-18y"),
                gender=random.choice(["Male", "Female", "Other"]),
                phone=fake.numerify(text="##########"),
                address=fake.address().replace("\n", ", "),
            )

            db.session.add(patient)
        patients.append(patient)

    db.session.commit()

                                 
    for doctor in doctors:
        for offset in range(0, 30, 3):                
            availability = DoctorAvailability(
                doctor=doctor,
                date=(datetime.utcnow() + timedelta(days=offset)).date(),
                start_time=time(9, 0),
                end_time=time(17, 0),
                slot_duration_minutes=30,
            )
            db.session.add(availability)

    db.session.commit()

                                       
    for _ in range(250):
        patient = random.choice(patients)
        doctor = random.choice(doctors)

        appt = Appointment(
            patient=patient,
            doctor=doctor,
            status=random.choice(["Booked", "Completed", "Cancelled"]),
            time=random_time_between(),
            date=random_date_in_range(90),
        )
        db.session.add(appt)
        db.session.flush()

        if appt.status == "Completed":
            treatment = Treatment(
                appointment_id=appt.id,
                diagnosis=fake.sentence(8),
                tests="Blood Test, X-Ray",
                prescription="Paracetamol 500mg, Vitamin C",
                medicines="Paracetamol, Vitamin C",
                visit_type="Follow-up",
                notes=f"Diet advice: {fake.vegetable()} + {fake.fruit()}",
            )
            db.session.add(treatment)

    db.session.commit()

                                                
    for _ in range(50):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        
                                         
        future_date = (datetime.utcnow() + timedelta(days=random.randint(1, 14))).date()
        
        appt = Appointment(
            patient=patient,
            doctor=doctor,
            status="Booked",
            time=random_time_between(),
            date=future_date,
        )
        db.session.add(appt)

    db.session.commit()

    print("DB Seeded Successfully:")
    print("- 1 Admin")
    print("- 10 Doctors")
    print("- 50 Patients")
    print("- Appointments spread across 90 days for time-series graphs")
    print("- Availability slots generated for each doctor")

if __name__ == "__main__":
    with app.app_context():
        seed()
