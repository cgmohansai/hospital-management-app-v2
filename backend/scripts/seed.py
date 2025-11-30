# scripts/seed_db.py

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
    # --- ROLES ---
    admin_role = get_or_create_role("admin", "Full access")
    doctor_role = get_or_create_role("doctor", "Registered medical professional")
    patient_role = get_or_create_role("patient", "Registered patient")
    
    # Cleanup manager role
    manager_role = Role.query.filter_by(name="manager").first()
    if manager_role:
        db.session.delete(manager_role)
        db.session.commit()

    # --- ADMIN USER ---
    create_user(
        username="admin",
        name="Admin User",
        email="admin@study",
        password="pass",
        roles=[admin_role],
    )

    # --- DEPARTMENTS ---
    dept_names = [
        "Cardiology",
        "Orthopedics",
        "Gastroenterology",
        "Oncology",
        "Gynecology",
        "Pediatrics",
        "KidneyTransplantation",
        "Liver Transplantation",
        "Pancreas Transplantation",
        "Urology",
        "Rheumatology",
        "Vascular Surgery",
        "Neurology",
        "Ophthalmology",
        "Dermatology",
        "Endocrinology",
        "Interventional Radiology",
        "Nephrology",
        "Organ Transplantation",
        "Robotic Surgery",
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

    # --- DOCTORS (10) ---
    doctors = []
    for i in range(10):
        full_name = fake.name()
        email = f"doctor{i+1}@study"
        username = f"doctor{i+1}"

        user = create_user(
            username=username,
            name=full_name,
            email=email,
            password="pass",
            roles=[doctor_role],
        )

        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if not doctor:
            specialization = random.choice(
                ["Cardiologist", "Neurologist", "Orthopedic", "Pediatrician", "Physician"]
            )

            doctor = Doctor(
                user_id=user.id,
                specialization=specialization,
                bio=fake.text(180),
                is_active=True,
                department=random.choice(departments),
            )
            db.session.add(doctor)
        doctors.append(doctor)

    db.session.commit()

    # --- PATIENTS (50) ---
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

    # --- DOCTOR AVAILABILITY ---
    for doctor in doctors:
        for offset in range(0, 30, 3):  # every 3 days
            availability = DoctorAvailability(
                doctor=doctor,
                date=(datetime.utcnow() + timedelta(days=offset)).date(),
                start_time=time(9, 0),
                end_time=time(17, 0),
                slot_duration_minutes=30,
            )
            db.session.add(availability)

    db.session.commit()

    # --- APPOINTMENTS + TREATMENTS ---
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
                prescription=", ".join([fake.dish(), fake.ingredient(), fake.spice()]),
                notes=f"Diet advice: {fake.vegetable()} + {fake.fruit()}",
            )
            db.session.add(treatment)

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
