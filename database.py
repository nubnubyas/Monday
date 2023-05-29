from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    # groups = db.relationship('Group', secondary='user_groups', backref='users')

class TravelActivities(Enum):
    HIKING = 'Hiking'
    SIGHTSEEING = 'Sightseeing'
    BEACH = 'Beach'

class Accommodation(Enum):
    HOTEL = 'Hotel'
    AIRBNB = 'Airbnb'
    HOSTEL = 'Hostel'

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_activities = db.Column(db.Enum(TravelActivities), nullable=False)
    accommodation = db.Column(db.Enum(Accommodation), nullable=False)
    budget = db.Column(db.Float, nullable=False)

class UserGroupPreference(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    travel_activities = db.Column


