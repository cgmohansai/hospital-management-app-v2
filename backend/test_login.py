import urllib.request
import json

base_url = "http://localhost:5000/api"

# 1. Login
login_url = f"{base_url}/auth/login"
login_payload = {
    "email": "admin@study",
    "password": "pass"
}
headers = {
    "Content-Type": "application/json"
}

print("Logging in...")
data = json.dumps(login_payload).encode('utf-8')
req = urllib.request.Request(login_url, data=data, headers=headers, method='POST')

token = None
try:
    with urllib.request.urlopen(req) as response:
        resp_body = response.read().decode('utf-8')
        print(f"Login Status: {response.getcode()}")
        resp_json = json.loads(resp_body)
        token = resp_json.get('token') or resp_json.get('response', {}).get('user', {}).get('authentication_token')
        # Flask-Security-Too might return it differently depending on config, but my previous test showed "token" at top level.
        print(f"Token received: {token is not None}")
except urllib.error.HTTPError as e:
    print(f"Login Failed: {e.code}")
    print(e.read().decode('utf-8'))
    exit(1)

if not token:
    print("No token found.")
    exit(1)

# 2. Add Doctor
# First create user via /auth/register (as per my frontend logic)
# Wait, my frontend logic for Add Doctor was:
# 1. POST /auth/register (create user)
# 2. POST /doctor (create profile)

# Let's replicate that.
register_url = f"{base_url}/auth/register"
new_doc_user = {
    "username": "testdoc_script",
    "email": "testdoc_script@test.com",
    "password": "pass",
    "name": "Test Doctor Script",
    "phone": "5555555555",
    "role": "doctor"
}

print("\nRegistering new doctor user...")
# We need to send the token? 
# /auth/register is usually public. But if I am admin adding it...
# The frontend calls it without token? No, api.js attaches token if present.
# But /auth/register might not need it.
# However, for "Add Doctor" functionality, we are just using the register endpoint.
# Let's try calling it.

reg_headers = headers.copy()
# reg_headers["Authorization"] = token # Register is public, usually.

data = json.dumps(new_doc_user).encode('utf-8')
req = urllib.request.Request(register_url, data=data, headers=reg_headers, method='POST')

new_user_id = None
try:
    with urllib.request.urlopen(req) as response:
        resp_body = response.read().decode('utf-8')
        print(f"Register Status: {response.getcode()}")
        resp_json = json.loads(resp_body)
        new_user_id = resp_json.get('id')
        print(f"New User ID: {new_user_id}")
except urllib.error.HTTPError as e:
    print(f"Register Failed: {e.code}")
    print(e.read().decode('utf-8'))
    exit(1)

# 3. Create Doctor Profile
doctor_url = f"{base_url}/doctors" # Resource is at /doctors (plural) based on __init__.py
# api.add_resource(DoctorListResource, "/doctors")

doc_profile_payload = {
    "user_id": new_user_id,
    "specialization": "Cardiology",
    "bio": "Created via script",
    "is_active": True
}

print("\nCreating doctor profile...")
doc_headers = headers.copy()
doc_headers["Authorization"] = token # This endpoint definitely needs auth (or maybe not? let's assume yes for admin)

data = json.dumps(doc_profile_payload).encode('utf-8')
req = urllib.request.Request(doctor_url, data=data, headers=doc_headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Create Profile Status: {response.getcode()}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"Create Profile Failed: {e.code}")
    print(e.read().decode('utf-8'))
