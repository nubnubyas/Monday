import os

from flask import Flask, flash, redirect, render_template, request, session
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    groups = db.relationship('Group', secondary=user_groups, backref='users')

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
    travel_activities = db.Column(db.Enum(TravelActivities), nullable=False)
    accommodation = db.Column(db.Enum(Accommodation), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref=db.backref('group_preferences', cascade='all, delete-orphan'))
    group = db.relationship('Group', backref=db.backref('user_preferences', cascade='all, delete-orphan'))

# Define a many-to-many relationship between users and groups
user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)


# functions
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirm password is the same
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password is not the same", 400)

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256')

        userz = db.execute("SELECT * FROM users")
        check = 0
        for i in userz:
            if i["username"] == request.form.get("username"):
                check += 1
                flash('Duplicate username')
        if check == 0:
            # remember users in database
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)

            # Redirect user to home page
            flash('You are successfully registered', 200)
            return render_template("login.html")
        else:

            return render_template("register.html"), 400
    else:
        return render_template("register.html")