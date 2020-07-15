![active development](https://img.shields.io/badge/active%20dev-no-red.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/simcard0000/HTN2020-backend-dev-challenge.svg)
# HTN2020-backend-dev-challenge

This is my submission! As this was my first time using SQL, SQL-related libraries, and Flask, there was a large learning curve - and so to help me complete this challenge, I referred to flask-sqlalchemy documentation from [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/) and [here](https://docs.sqlalchemy.org/en/13/index.html), as well as a few Stack Overflow questions/tutorials such as [this](https://stackoverflow.com/questions/1378325/python-dicts-in-sqlalchemy) and [this](https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12) while I debugged.

### Queries
- To get information on all users: `GET localhost:5000/users`
- To get information on a specific user: `GET localhost:5000/users/3`, where the number is the user_id
- To get information on users within a certain range of latitude and longitude: `GET localhost:5000/users?lat=48.4862&long=-34.7754&range=0.1`
- To get information on all events: `GET localhost:5000/events`
- To get information on a specific event: `GET localhost:5000/events/1`, where the number is the event_id
- To add an attendee to an event: `PUT localhost:5000/events/3/attendees`, where the number is the event_id and sent with a payload as defined in the problem statement

### Improvements
- Noticed in the JSON file given with the user profiles there a lot of emails that did not match up with names. I ended up just putting the JSON as is into the "Users" table, but fixing this would be the first thing I would do.
- As I make use of two tables (Users and Events), implementing foreign keys would make adding and removing people more easier.
- Looking back, using SQLAlchemy was probably a bit too intense for this challenge (being an object-relational mapper), and I could have definetely made the database with just SQLite3, allowing me to use SQL commands instead of the functions SQLAlchemy provided (which do correspond back to SQL)

Thanks for considering me!
