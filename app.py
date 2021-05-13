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

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

document = uuids.find_one({})

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    # return user_uuid in users_sessions
    return uuids.find()

# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
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

    if users.update({'username': data['username'], 'password':data['password']},data, upsert=True,): 
        return Response(data['username']+" was added to the MongoDB", mimetype='application/json'),200 # ΠΡΟΣΘΗΚΗ STATUS
    else:
        return Response("A user with the given email already exists", mimetype='application/json'),400 # ΠΡΟΣΘΗΚΗ STATUS

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

    if(is_session_valid(document)):
        student = list(students.find({'email': data['email']}))
            # Η παρακάτω εντολή χρησιμοποιείται μόνο στη περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχει φοιτητής με αυτό το email).
        return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json')
    else:
        return Response("Log in first",mimetype='application/json'),400 

# ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():
    if(is_session_valid(document)):
        student = list(students.find({'yearOfBirth': 1991}))
        return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json')
    else:
        return Response("Log in first",mimetype='application/json'),400 

# ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_thirty1():
    if(is_session_valid(document)):
        student = list(students.find({'yearOfBirth': {"$gt":1990}}))
        return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json')
    else:
        return Response("Log in first",mimetype='application/json') 

# ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email 
@app.route('/getStudentAddress', methods=['GET'])
def get_student1():
    # Request JSON data
    student = {}
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
        if students.find_one({'email': data['email'], "address": {"$exists":True}}):
            student = students.find_one({'email': data['email']}, {'_id':0 ,'name': 1, 'address.street':1, 'address.postcode':1})
            return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json') 
        else:
            return "No address found"
    else:
        return Response("Log in first",mimetype='application/json') 

# ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email 
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
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
        if students.find_one({'email': data['email']}):
            students.delete_one({'email': data['email']})
            msg = "student deleted"
            return Response(msg, status=200, mimetype='application/json')
        else:
            return "No address found"
    else:
        return Response("Log in first",mimetype='application/json') 

# ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email 
@app.route('/addCourses', methods=['PATCH'])
def add_courses():
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
    
    courses = [
        data["courses"]
    ]

    if(is_session_valid(document)):
        if students.find_one({'email': data['email']}):
            students.update({'email': data['email']}, {'$set': {'courses': courses}})
            msg = "courses added"
            return Response(msg, status=200, mimetype='application/json')
        else:
            return "No address found"
    else:
        return Response("Log in first",mimetype='application/json') 

# ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email
@app.route('/getPassedCourses', methods=['GET'])
def get_courses():
    # Request JSON data
    student = {}
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
        if students.find_one({'email': data['email'], "courses": {"$exists":True}}):
            student = students.find_one({'email': data['email']}, {'_id':0 ,'name': 1, 'courses': 1 })
            return Response(json.dumps(student, default=json_util.default), status=200, mimetype='application/json') 
        else:
            return "No address found"
    else:
        return Response("Log in first",mimetype='application/json') 

# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)