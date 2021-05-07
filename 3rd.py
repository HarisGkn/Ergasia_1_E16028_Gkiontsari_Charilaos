from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
from bson import json_util
import json
import uuid
import time

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['InfoSys']

# Choose collections
students = db['Students']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

# ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email 
@app.route('/getStudent', methods=['GET'])
def get_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
# session validation to be added
    student = list(students.find({'email': data['email']}))
    for data in student:
        print(data)
    
    # Η παρακάτω εντολή χρησιμοποιείται μόνο στη περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχει φοιτητής με αυτό το email).
    return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json')

# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)