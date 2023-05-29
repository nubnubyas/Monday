import os

from flask import Flask, flash, redirect, render_template, request, session
from database import db, User, Group, UserGroupPreference
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

user = User(id = 1, username="testname", password="testpw")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     groups = db.relationship('Group', secondary=user_groups, backref='users')

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
#     travel_activities = db.Column(db.Enum(TravelActivities), nullable=False)
#     accommodation = db.Column(db.Enum(Accommodation), nullable=False)
#     budget = db.Column(db.Float, nullable=False)
#     user = db.relationship('User', backref=db.backref('group_preferences', cascade='all, delete-orphan'))
#     group = db.relationship('Group', backref=db.backref('user_preferences', cascade='all, delete-orphan'))

# # Define a many-to-many relationship between users and groups
# user_groups = db.Table('user_groups',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
# )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/group", methods=["GET", "POST"])
def group():
    return render_template("group.html")

@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    return render_template("questionnaire.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)