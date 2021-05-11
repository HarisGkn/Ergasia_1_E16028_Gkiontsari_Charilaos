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
uuids = db['uuid']

uuids.delete_many({})

document = uuids.find_one({})

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    # return user_uuid in users_sessions
    return uuids.find_one({})

# ΕΡΩΤΗΜΑ 2: Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")


    if users.find({ "username" : data['username'], "password" : data['password']} ).count() > 0: 
        user_uuid = create_session(data['username'])
        res = {"uuid": user_uuid, "username": data['username']}
        uuids.insert_one({'username': data['username'] ,"uuid": user_uuid})
        return Response(json.dumps(res), mimetype='application/json'),200 # ΠΡΟΣΘΗΚΗ STATUS
    else:
        # Μήνυμα λάθους (Λάθος username ή password)
        return Response("Wrong username or password.",mimetype='application/json'),400 # ΠΡΟΣΘΗΚΗ STATUS

# ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email 
@app.route('/getStudentAddress', methods=['GET'])
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

    if(is_session_valid(document)):
        # student = list(students.find({'yearOfBirth': {"$gt":1990}}))
        return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json')
    else:
        return Response("Log in first",mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS



# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)