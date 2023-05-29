# from flask_sqlalchemy import SQLAlchemy
# from enum import Enum

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     # groups = db.relationship('Group', secondary='user_groups', backref='users')

# class TravelActivities(Enum):
#     HIKING = 'Hiking'
#     SIGHTSEEING = 'Sightseeing'
#     BEACH = 'Beach'

# class Accommodation(Enum):
#     HOTEL = 'Hotel'
#     AIRBNB = 'Airbnb'
#     HOSTEL = 'Hostel'

# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     travel_activities = db.Column(db.Enum(TravelActivities), nullable=False)
#     accommodation = db.Column(db.Enum(Accommodation), nullable=False)
#     budget = db.Column(db.Float, nullable=False)

# class UserGroupPreference(db.Model):
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
#     travel_activities = db.Column

import sqlite3

# create a connection to the database (or create the database if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# create a cursor object to execute SQL queries
cursor = conn.cursor()

# create a table for users
cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')

# insert some data into the users table
cursor.execute('INSERT INTO users VALUES (1, "Alice", "alice@example.com")')
cursor.execute('INSERT INTO users VALUES (2, "Bob", "bob@example.com")')
cursor.execute('INSERT INTO users VALUES (3, "Charlie", "charlie@example.com")')

# # create a table for groups
cursor.execute('CREATE TABLE groups (id INTEGER PRIMARY KEY, name TEXT, description TEXT)')

# # insert some data into the groups table
# cursor.execute('INSERT INTO groups VALUES (1, "Group 1", "This is group 1")')
# cursor.execute('INSERT INTO groups VALUES (2, "Group 2", "This is group 2")')
# cursor.execute('INSERT INTO groups VALUES (3, "Group 3",... "This is group 3")')

# commit the changes to the database
conn.commit()

# close the cursor and the connection
cursor.close()
conn.close()
