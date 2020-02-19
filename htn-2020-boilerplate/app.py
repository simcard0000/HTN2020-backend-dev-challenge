from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
from apiclient import errors
from apiclient import http
import sqlite3

#initializing the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db_editing = SQLAlchemy(app)
ma = Marshmallow(app)

#first, check if table exists

#If not, use the local json file to set up the table


#create IDs for each user and relate them in the table

#parts of the Flask app: all users endpoint (return a list of all user data in JSON);
#return data on a specific user, A special location query should be able to find and 
# return a list of users within a certain range of a specified latitude and longitude.

#Take initial JSON file and create a table for just events

#then other parts of the flask app: get event data for a specific event,
# (link attendees and events), and add an attendee to an event

#document endpoints and create a README of what's been done and what to improve!


