from app import create_app
from extensions import db
from services.doctor_service import DoctorService
from models import Doctor, User
import traceback

app = create_app()

with app.app_context():
    print("--- Debugging DoctorService ---")
    try:
                          
        doc = Doctor.query.first()
        if not doc:
            print("No doctor found.")
            exit()
            
        print(f"Found Doctor ID: {doc.id}, User ID: {doc.user_id}, Name: {doc.user.name}")
        
                                 
        print("\n--- Testing Status Update ---")
        update_data = {
            "id": doc.id,
            "is_active": not doc.is_active
        }
        print(f"Updating with: {update_data}")
        updated_doc = DoctorService.update(update_data)
        print(f"Update success. New Active Status: {updated_doc.is_active}, User Active: {updated_doc.user.active}")
        
                                  
        print("\n--- Testing Details Update ---")
        details_data = {
            "id": doc.id,
            "name": "Updated Debug Name",
            "phone": "1112223333",
            "specialization": "Debug Spec"
        }
        print(f"Updating with: {details_data}")
        updated_doc_2 = DoctorService.update(details_data)
        print(f"Update success. Name: {updated_doc_2.user.name}, Phone: {updated_doc_2.phone}")

                        
                                         
        print("\n--- Creating Dummy Doctor for Delete Test ---")
                              
        from flask_security.utils import hash_password
        user = User(
            username="todelete",
            email="todelete@test.com",
            name="To Delete",
            password=hash_password("pass"),
            active=True
        )
        db.session.add(user)
        db.session.commit()
        
        doc_to_delete = Doctor(
            user_id=user.id,
            specialization="DeleteMe",
            phone="0000000000",
            is_active=True
        )
        db.session.add(doc_to_delete)
        db.session.commit()
        print(f"Created Doctor ID: {doc_to_delete.id}")
        
        print("\n--- Testing Delete ---")
        DoctorService.delete(doc_to_delete.id)
        print("Delete success.")
        
                         
        deleted_doc = Doctor.query.get(doc_to_delete.id)
        deleted_user = User.query.get(user.id)
        print(f"Doc exists: {deleted_doc is not None}")
        print(f"User exists: {deleted_user is not None}")

    except Exception:
        print("EXCEPTION CAUGHT:")
        traceback.print_exc()
