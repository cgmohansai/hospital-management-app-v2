from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

appointments_data = [{'hi': 2}, {'hello': 5}] 

@app.route("/appointments")
def get_appointments(): 
    return jsonify(appointments_data)

if __name__ == "__main__":
    app.run(debug=True)
