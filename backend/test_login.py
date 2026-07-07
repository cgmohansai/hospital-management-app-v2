import urllib.request
import json

base_url = "http://localhost:5000/api"

          
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
                                                                                                                               
        print(f"Token received: {token is not None}")
except urllib.error.HTTPError as e:
    print(f"Login Failed: {e.code}")
    print(e.read().decode('utf-8'))
    exit(1)

if not token:
    print("No token found.")
    exit(1)

               
                                                                 
                                             
                                      
                                  

                       
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
                             
                                                                  
                                                                            
                                       
                                                                                   
                       

reg_headers = headers.copy()
                                                                     

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

                          
doctor_url = f"{base_url}/doctors"                                                        
                                                  

doc_profile_payload = {
    "user_id": new_user_id,
    "specialization": "Cardiology",
    "bio": "Created via script",
    "is_active": True
}

print("\nCreating doctor profile...")
doc_headers = headers.copy()
doc_headers["Authorization"] = token                                                                                 

data = json.dumps(doc_profile_payload).encode('utf-8')
req = urllib.request.Request(doctor_url, data=data, headers=doc_headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Create Profile Status: {response.getcode()}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"Create Profile Failed: {e.code}")
    print(e.read().decode('utf-8'))
