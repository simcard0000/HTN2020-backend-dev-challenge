from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import json

#Initializing the Flask app
app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Defining the schema
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    user_name = db.Column('name', db.String(100))
    picture = db.Column('picture', db.String(100))
    company = db.Column('company', db.String(100))
    email = db.Column('email', db.String(100))
    phone = db.Column('phone', db.String(100))
    latitude = db.Column('latitude', db.Float)
    longitude = db.Column('longitude', db.Float)
    events = db.Column('events', db.JSON)

    def __init__(self, user_id, user_name, picture, company, email, phone, latitude, longitude, events):
        self.user_id = user_id
        self.user_name = user_name
        self.picture = picture
        self.company = company
        self.email = email
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude
        self.events = events

class Event(db.Model):
    __tablename__ = 'Events'
    event_name = db.Column('event_name', db.String(100))
    event_id = db.Column('event_id', db.Integer, primary_key = True)
    attendees = db.Column('attendees', db.PickleType)

    def __init__(self, event_name, event_id, attendees):
        self.event_name = event_name
        self.event_id = event_id
        self.attendees = attendees

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_name', 'picture', 'company', 'email', 'phone', 'latitude', 'longitude', 'events')

class EventSchema(ma.Schema):
    class Meta:
        fields = ('event_name', 'event_id', 'attendees')

user_schema = UserSchema()
users_schema = UserSchema(many = True)
event_schema = EventSchema()
events_schema = EventSchema(many = True)

assign_user_id = 0
assign_event_id = 0
attendee_list = []
user_dict = {}

db.create_all()

#Populating the tables
with (open('data.json')) as json_file:
    data = json.load(json_file)
    for i in data:
        new_user = User(assign_user_id, i['name'], i['picture'], i['company'], 
            i['email'], i['phone'], i['latitude'], i['longitude'], i['events'])
        for things in i['events']:
            if (db.session.query(db.session.query(Event).filter_by(event_name=things['name']).exists()).scalar() == False):
                user_dict = {}
                attendee_list = []
                user_dict['name'] = i['name']
                user_dict['id'] = assign_user_id
                attendee_list.append(user_dict)
                new_event = Event(str(things['name']), int(assign_event_id), attendee_list)
                db.session.add(new_event)
                assign_event_id += 1
            else:
                all_events = Event.query.all()
                for event in all_events:
                    if (event.event_name == things['name']):
                        user_dict = {}
                        user_dict['name'] = i['name']
                        user_dict['id'] = assign_user_id
                        ret_list = list(event.attendees)
                        ret_list.append(user_dict)
                        event.attendees = ret_list
                        db.session.commit()
        db.session.add(new_user)
        db.session.commit()
        assign_user_id += 1

#data on a specific user
#GET localhost:5000/users/<id>
@app.route('/users/<id>', methods=['GET'])
def specific_user(id):
    the_user = User.query.get(id)
    return user_schema.jsonify(the_user)

#list of users within a certain range of latitude and longitude, or all users
#GET localhost:5000/users?lat=48.4862&long=-34.7754&range=0.1
#GET localhost:5000/users
@app.route('/users', methods=['GET'])
def lat_long():
    input_latitude = request.args.get('lat')
    input_longitude = request.args.get('long')
    input_range = request.args.get('range')
    if (input_latitude is None and input_longitude is None and input_range is None):
            all = User.query.all()
            result = users_schema.dump(all)
            return jsonify(result)
    else:
        bottom = float(input_latitude) - float(input_range)
        top = float(input_latitude) + float(input_range)
        bottom2 = float(input_longitude) - float(input_range)
        top2 = float(input_longitude) + float(input_range)
        satisfy = db.session.query(User).filter(User.latitude >= bottom, User.latitude <= top,
            User.longitude >= bottom2, User.longitude <= top2).all()
        result = users_schema.dump(satisfy)
        return jsonify(result)
        
#add an attendee to an event
#PUT localhost:5000/events/3/attendees with payload
@app.route('/events/<id3>/attendees', methods=['PUT'])
def add_attendee(id3):
    user_dict = {}
    attendee_id = request.json['user_id']
    the_user = User.query.get(attendee_id)
    the_event = Event.query.get(id3)
    user_dict['name'] = the_user.user_name
    user_dict['id'] = the_user.user_id
    ret_list = list(the_event.attendees)
    ret_list.append(user_dict)
    the_event.attendees = ret_list
    data = list(the_user.events)
    data.append({'name': the_event.event_name})
    the_user.events = data
    db.session.commit()
    the_event = Event.query.get(id3)
    return event_schema.jsonify(the_event)

#get data for a specific event
#GET localhost:5000/events/1
@app.route('/events/<id2>', methods=['GET'])
def specific_event(id2):
    the_event = Event.query.get(id2)
    return event_schema.jsonify(the_event)

#get data for all events
#GET localhost:5000/events
@app.route('/events/', methods=['GET'])
def all_events():
    all = Event.query.all()
    result = events_schema.dump(all)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=TRUE)
