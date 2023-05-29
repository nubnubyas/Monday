import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
# from database import db, User, Group, UserGroupPreference
from enum import Enum
from flask_session import Session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# init Object classes and establish relationships
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.preferences = []

class Group:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.users = []
        self.activities = []
        self.accommodations = []

class Activity:
    def __init__(self, name):
        self.name = name

class Accommodation:
    def __init__(self, name):
        self.name = name

class UserPreference:
    def __init__(self, userid, groupid, accommodationType, accommodationPrice, transportationMode, transportationBudget, activityType, activityBudget, destinationCountry, destinationBudget):
        self.user = userid
        self.group = groupid
        self.accommodationType = accommodationType 
        self.accommodationPrice = accommodationPrice 
        self.transportationMode = transportationMode 
        self.transportationBudget = transportationBudget 
        self.activityType = activityType 
        self.activityBudget = activityBudget 
        self.destinationCountry = destinationCountry 
        self.destinationBudget = destinationBudget

# create a connection to the database (or create the database if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL)''')

# not rly used
cursor.execute('''CREATE TABLE IF NOT EXISTS users_groups (
                    user_id INTEGER,
                    group_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_id INTEGER,
                    FOREIGN KEY (group_id) REFERENCES groups (id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS accommodations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_id INTEGER,
                    FOREIGN KEY (group_id) REFERENCES groups (id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    userid INTEGER,
                    groupid INTEGER,
                    accommodationType TEXT,
                    accommodationPrice REAL,
                    transportationMode TEXT,
                    transportationBudget REAL,
                    activityType TEXT,
                    activityBudget REAL,
                    destinationCountry TEXT,
                    destinationBudget REAL,
                    FOREIGN KEY (userid) REFERENCES users (id),
                    FOREIGN KEY (groupid) REFERENCES groups (id))''')

# Insert data
def insert_user(user):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
    user.id = cursor.lastrowid
    a = user.id
    conn.commit()
    conn.close()
    return a

def insert_group(group):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groups (name, password) VALUES (?, ?)", (group.name, group.password))
    group.id = cursor.lastrowid
    a = group.id
    for user in group.users:
        cursor.execute("INSERT INTO users_groups (user_id, group_id) VALUES (?, ?)", (user.id, group.id))
    for activity in group.activities:
        cursor.execute("INSERT INTO activities (name, group_id) VALUES (?, ?)", (activity.name, group.id))
    conn.commit()
    conn.close()
    return a

def insert_user_preference(user_preference):
    cursor.execute("INSERT INTO user_preferences (userid, groupid, accommodationType, accommodationPrice, transportationMode, transportationBudget, activityType, activityBudget, destinationCountry, destinationBudget) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (user_preference.userid, user_preference.groupid, user_preference.accommodationType, 
                    user_preference.accommodationPrice, user_preference.transportationMode, user_preference.transportationBudget, user_preference.activityType, user_preference.activityBudget, 
                    user_preference.destinationCountry, user_preference.destinationBudget))
    user_preference.id = cursor.lastrowid

# Create objects for reference (to be removed)
user1 = User("John", "password1")
user2 = User("Jane", "password2")

group1 = Group("Group 1", "group1password")
group2 = Group("Group 2", "group2password")

activity1 = Activity("Activity 1")
activity2 = Activity("Activity 2")

accommodation1 = Accommodation("Accommodation 1")
accommodation2 = Accommodation("Accommodation 2")

# preference1 = UserPreference(user1, group1, "Hotel", 100, "Luxury")
# preference2 = UserPreference(user2, group1, "Apartment", 50, "Budget")

# Establish relationships
group1.users.append(user1)
group1.users.append(user2)
group1.activities.append(activity1)
group1.activities.append(activity2)
group1.accommodations.append(accommodation1)
group1.accommodations.append(accommodation2)

# user1.preferences.append(preference1)
# user2.preferences.append(preference2)

# Insert data into the database
# insert_user(user1)
# insert_user(user2)
# insert_group(group1)
# insert_group(group2)
# insert_user_preference(preference1)
# insert_user_preference(preference2)

# Commit changes
conn.commit()
conn.close()
    
    # sequence of code to add to update the table
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()

    # # Perform the database operations
    # # ...

    # # Commit the changes
    # conn.commit()

    # # Close the connection
    # conn.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/group", methods=["GET", "POST"])
def group():
    if request.method == "POST":
        user_id = session.get("user_id")
        name = request.form.get("group-name")
        pw = request.form.get("group-password")
        group = Group(name, pw)
        group_id = insert_group(group)
        print(user_id)
        print(group_id)
        return redirect(url_for('questionnaire', group_id = group_id))
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("group.html")

@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    user_id = session.get("user.id")
    group_id = request.args.get('group_id')
    print(user_id)
    print(group_id)
    if request.method == "POST":
        accommodation_type = request.form['accommodation-type']
        accommodation_price = int(request.form['accommodation-price'])
        transportation_mode = request.form['transportation-mode']
        transportation_budget = int(request.form['transportation-budget'])
        activity_type = request.form.getlist('activity-type')
        activity_budget = int(request.form['activity-budget'])
        destination_country = request.form['destination-country']
        destination_budget = int(request.form['destination-budget'])
        p = UserPreference(user_id, group_id, accommodation_type, accommodation_price, transportation_mode, transportation_budget, activity_type, activity_budget, destination_country, destination_budget)
        insert_user_preference(p)
        return redirect(url_for('home', user_id = user_id, group_id = group_id))
    else :
        return render_template("questionnaire.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        pw = request.form.get("password")
        user = User(username, pw)
        user_id = insert_user(user)
        session["user_id"] = user_id
        print(session.get("user_id"))
        # Redirect user to home page
        return redirect("/group")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)