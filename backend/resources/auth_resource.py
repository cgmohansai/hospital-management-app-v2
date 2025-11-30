"/login"
"/register"

from flask import Blueprint, jsonify, request
from flask_security.utils import verify_password, hash_password

from models import User, Patient, db

from flask import current_app

auth_bp = Blueprint("auth",__name__, url_prefix="/api/auth") #whole auth related routes will be here


@auth_bp.route("/login", methods=['POST'])
def login():

    data = request.get_json()

    username_or_email = data["username"] or data.get("email") # cuz it was mentioned in the doc, user can use both 
    password = data["password"]

    if (not username_or_email or not password):
        return jsonify({"message": "Invalid input"}), 400
    
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first_or_404() 
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not verify_password(password, user.password):
        return jsonify({'message': 'Wrong password!'}), 400
    
    role_names = [role.name for role in user.roles] if user.roles else []     #getting user role for response
    
    return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "roles": role_names,
            "token": user.get_auth_token(),
        }), 200


@auth_bp.route("/register", methods=['POST'])
def register():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')  
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role', 'patient')  

    if not username or not password or not name or not email or not phone:
        return jsonify({"message": "Invalid inputs"}), 400

    if role not in ["patient", "doctor"]:#only patient and doctor are allowed to register
        return jsonify({"message": "Invalid role. Only 'patient' or 'doctor' allowed"}), 400

    datastore = current_app.datastore

    if User.query.filter_by(username=username).first(): #cheking if username already present
        return jsonify({"message": "Username already exists"}), 400
    
    if User.query.filter_by(email=email).first(): # if email already present
        return jsonify({"message": "Email already exists"}), 400

    active = True
    if role == "doctor":
        active = False  #doctors need admin approval

    #creating user with given role
    try:
        
        user = datastore.create_user(  #creating user with flask security attributes
            username=username,
            name=name,
            email=email,
            password=hash_password(password),
            active=active
        )
        db.session.flush()  # Flush is used to get user.id
        
        #find or create the role
        user_role = datastore.find_or_create_role(role, description=f"{role.capitalize()} User")
        #adding role to user
        datastore.add_role_to_user(user, user_role)
        
        #patient profile creation
        if role == "patient":
            patient = Patient(
                user_id=user.id,
                phone=phone
            )
            db.session.add(patient)
        
        db.session.commit()
        
        message = f"{role.capitalize()} Registered Successfully"
        if role == "doctor":
            message += ". Your account is pending admin approval."
        
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "phone": phone,
            "role": role,
            "active": active,
            "message": message
        }), 201
        
    except:
        db.session.rollback()
        return jsonify({"message": "Error during registration"}), 400