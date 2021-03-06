import os
import sys
import json
import requests
import flask_sqlalchemy
import time
from flask import Flask, render_template, request, jsonify, abort, make_response

from twilio.rest import Client
app = Flask(__name__)

import models

#for heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'

db = flask_sqlalchemy.SQLAlchemy(app)

# for twilio
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

# Find these values at https://twilio.com/user/account

client = Client(account_sid, auth_token)

# client.messages.create(
#     to="+18314285108",
#     from_="+18313461202",
#     body="This is the ship that made the Kessel Run in fourteen parsecs?")

#import models

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/saltest', methods = ['POST', 'GET'])
def saltest():
    aUserID = "DIiWPEoJQldpzoi6qrXNH5WzqO02"
    locationInDB = models.Location.query.filter_by(userID=aUserID).first()
    latitude = ""
    longitude = ""
    
    log(locationInDB)
    
    if locationInDB is not None:
        for row in locationInDB:
            # print row.owed_ID
            latitude = row.latitude
            longitude = row.longitude
            break
    return "saltest"
    
@app.route('/api/v1.0/postInfo', methods=['POST'])
def create_task():
    log("someone pinged the postInfo api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    locationData = {
        'userID': request.json['userID'],
        'latitude': request.json['latitude'],
        'longitude': request.json['longitude'],
        'timestamp' : str(int(time.time()))
    }
    
    aUserID = request.json['userID']
    #if user is not in the locations, then add, else 
    locationInDB = models.Location.query.filter_by(userID=aUserID).first()
    log(locationInDB)
    row = locationInDB
    if locationInDB is None:
        #insert
        new_location = models.Location(request.json['userID'], 
                                float(request.json['latitude']), 
                                float(request.json['longitude']), 
                                str(int(time.time()))
        )
        models.db.session.add(new_location)
        models.db.session.commit()
    #update
    else:
        lat = request.json['latitude']
        lon = request.json['longitude']
        
        models.Location.query.filter_by(userID=aUserID).update(dict(latitude=lat, longitude=lon))
        models.db.session.commit()
        
    # #tasks.append(task)
    return jsonify({'data': locationData}), 200
    
@app.route('/api/v1.0/signup', methods=['POST'])
def signup():
    log("someone pinged signup api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    userData = {
        'userID': request.json['userID'],
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
        'email': request.json['email'],
        'phoneNumber': request.json['phoneNumber'],
        'timestamp' : request.json['timestamp'],
        'imgURL' : request.json['imgURL'],
    }
    
    new_user = models.Users(userData['userID'], 
                            userData['firstName'], 
                            userData['lastName'], 
                            userData['email'],
                            userData['imgURL'],
                            userData['phoneNumber']
    )
    models.db.session.add(new_user)
    models.db.session.commit()
    return jsonify({'data': userData}), 200
    
@app.route('/api/v1.0/login', methods=['POST'])
def login():
    log("someone pinged login the api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    userData = {
        'userID': request.json['userID'],
    }
    
    userSignedUp = {
            'userID': 'false'
        }
    
    user_ids = []
    message = models.Users.query.with_entities(models.Users.user_id).all()
    
    for theId in message:
        log(theId[0])
        user_ids.append(str(theId[0]))
    
    if str(userData['userID']) in user_ids:
        userSignedUp = {
            'userID': 'true'
        }
    else:
        userSignedUp = {
            'userID': 'false'
        }
        
    #tasks.append(task)
    #return jsonify({'data': {'userID': 'true'}}), 200
    log({'data': userSignedUp})
    return jsonify({'data': userSignedUp}), 200

@app.route('/api/v1.0/send', methods=['POST'])
def send():
    log("someone pinged send the api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    
    userData = {
        'userID': request.json['userID'],
    }
    
    # client.messages.create(
    # to="+18314285108",
    # from_="+18313461202",
    # body="This is the ship that made the Kessel Run in fourteen parsecs?")
    
    message = "this user has not contacted us with in the last 30min"
    
    return jsonify({'status': 'success'}), 200
    
@app.route('/api/v1.0/startDate', methods=['POST'])
def startDate():
    log("someone pinged startDate the api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    

    userID = request.json['userID']
        
        
    #parses through the chaperones
    ###############################################
    try:
        chapCount = 1
        info = request.json['chaperones']
        log(info)
        d = json.loads(info)
        
        for key,val in d.iteritems():
            for chap in val:
                log("chaperone "+str(chapCount)+": "+chap['name'])
                log("phone number: "+chap['phone_number'])
                
                #adds values to chaperones table
                ts = str(int(time.time()))
                aChap = models.Chap(userID, chap['name'], chap['phone_number'], ts)
                models.db.session.add(aChap)
                models.db.session.commit()
                
                chapCount = chapCount + 1
                
    except KeyError:
        log("keyerror from chaperone payload")
    
    ###################################################
        
        #chaps = request.json['userID']['chap']
        
        #ts = str(int(time.time()))
        # for chap in chaps:
        #     chap = models.Chap(userID, chap['name'], chap['number'], ts)
        #     models.db.session.add(chaps)
         
        #  models.db.session.commit()
    
    return jsonify({'status': 'success'}), 200
    
@app.route('/api/v1.0/endDate', methods=['POST'])
def endDate():
    log("someone pinged the endDate api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    
    userID = request.json['userID']
    
    #deletes all chaperones associated with that user    
    models.Chap.query.filter_by(user_id=request.json['userID']).delete()
    models.db.session.commit()
    
    return jsonify({'status': 'success'}), 200
    
@app.route('/api/v1.0/emergency', methods=['POST'])
def emergency():
    log("someone pinged the emergency api")
    log(request.json)
    
    #if the json data does not have the 'usedID' header
    #it will return a 400
    if not request.json or not 'userID' in request.json:
        abort(400)
    
    userData = {
        'userID': request.json['userID'],
    }
    
    # message = userData['message']
    # message = "this user has not contacted us with in the last 30min"
    
    aUserID = request.json['userID']
    
    #get the last location from the user
    locationInDB = models.Location.query.filter_by(userID=aUserID).first()
    theUser = models.Users.query.filter_by(user_id=aUserID).first()
    latitude = ""
    longitude = ""
    
    if locationInDB is not None:
            # print row.owed_ID
            latitude = locationInDB.latitude
            longitude = locationInDB.longitude
    else:
        return jsonify({'status': 'fail'}), 200
    
    chapsInDB = models.Chap.query.filter_by(user_id=aUserID).all()
    log(chapsInDB)
    if chapsInDB is not None:
        for row in chapsInDB:
            # print row.owed_ID
            # str(row.user_id)
            # str(row.chapName)
            # str(row.chapNumber)
            
            message = str(theUser.firstName) +" "+str(theUser.lastName)+ " has not checked in with RendeVu. They may be in distress. This is their last location: "+str(latitude)+", "+str(longitude)
            message = message + "\nhttp://maps.google.com/maps?&z=5&q="+str(latitude)+"+"+str(longitude)+"&ll="+str(latitude)+"+"+str(longitude)
            log(row.chapNumber)
            
            client.messages.create(
            to="+1"+ str(row.chapNumber),
            from_="+18313461202",
            body=message)
    else:
        return jsonify({'status': 'fail'}), 200
    
    # message = request.json['userID'] + " Has not checked in and the sevices has not recieved a location you might want to call them their last location was"
    # client.messages.create(
    # to="+1"+"6197345766",
    # from_="+18313461202",
    # body=message)
    
    return jsonify({'status': 'success'}), 200

@app.route('/')
def hello():
    return "Hello world", 200

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )