import flask_sqlalchemy, app

#for heroku
app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
#app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://payinvader:girlscoutcookies1@localhost/postgres'

db = flask_sqlalchemy.SQLAlchemy(app.app)


class Users(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)  # key
    user_id = db.Column(db.String(200))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(200))
    imgUrl = db.Column(db.String(300))
    phoneNumber = db.Column(db.String(20))

    def __init__(self, user_id, firstName, lastName, email, imgUrl, phoneNumber):
        
        self.user_id = user_id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.imgUrl = imgUrl
        self.phoneNumber = phoneNumber

    def __repr__(self):
        return '%s %s %s %s %s %s' % (self.user_id, self.firstName, self.lastName, self.email, self.imgUrl, self.phoneNumber)
        
        
class Location(db.Model):
    __tablename__ = 'location_table'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    userID = db.Column(db.String(200))#requester
    latitude = db.Column(db.Float)#requestee
    longitude = db.Column(db.Float())
    time_stamp = db.Column(db.String(30))
    
    def __init__(self, userID, latitude, longitude, time_stamp):
    
    
        self.userID = userID
        self.latitude = latitude
        self.longitude = longitude
        self.time_stamp = time_stamp
    
    def __repr__(self):
        return '%s %s %s %s' % (self.userID, self.latitude, self.longitude, self.time_stamp)
        
class Confort(db.Model):
    __tablename__ = 'confort_table'
    
    id = db.Column(db.Integer, primary_key=True)  # key
    userID = db.Column(db.String(200)) 
    confortLevel = db.Column(db.Integer) 
    
    
    def __init__(self, userID, confortLevel):
    
        self.userID = userID
        self.confortLevel = confortLevel

    
    def __repr__(self):
        return '%d %d' % (self.userID, self.confortLevel)
        
class Chap(db.Model):
    __tablename__ = 'chap_table'

    id = db.Column(db.Integer, primary_key=True)  # key
    user_id = db.Column(db.String(200))
    chapName = db.Column(db.String(50))
    chapNumber = db.Column(db.String(50))
    ts = db.Column(db.String(50))


    def __init__(self, user_id, chapName, chapNumber, ts):
        
        self.user_id = user_id
        self.chapName = chapName
        self.chapNumber = chapNumber
        self.ts = ts

    def __repr__(self):
        return '%s %s %s %s' % (self.user_id, self.chapName, self.chapNumber, self.ts)
        