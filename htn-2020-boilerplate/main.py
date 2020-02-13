from flask import Flask
import sqlite3
conn = sqlite3.connect('hackers.db')

app = Flask(__name__)

@app.route('/')

#First, add user profiles by making an HTTP request to the given link

c = conn.cursor()

#Conduct a check to see if the table exists, if so skip creation and loading of data

c.execute('''CREATE TABLE Users
    (Username       Name VARCHAR(300), 
    Picture     VARCHAR(300), 
    Company     VARCHAR(300),
    Email       VARCHAR(300),
    Phone       VARCHAR(300)
    Latitude    float
    Longitude   float
    UserID      smallint)''')
    #connect events to users -> and link this table to another table just for events

c.execute('''CREATE TABLE Events
    (EventName   VARCHAR(300),
    EventID     smallint
    Attendees   )''')



