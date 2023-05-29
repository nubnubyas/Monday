import os

from flask import Flask, flash, redirect, render_template, request, session
# from database import db, User, Group, UserGroupPreference
from enum import Enum
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

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
    def __init__(self, user, group, accommodation_preference, budget_preference, travel_style_preference):
        self.user = user
        self.group = group
        self.accommodation_preference = accommodation_preference
        self.budget_preference = budget_preference
        self.travel_style_preference = travel_style_preference

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
                    user_id INTEGER,
                    group_id INTEGER,
                    accommodation_preference TEXT,
                    budget_preference REAL,
                    travel_style_preference TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (group_id) REFERENCES groups (id))''')

# Insert data
def insert_user(user):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
    user.id = cursor.lastrowid
    conn.commit()
    conn.close()

def insert_group(group):
    cursor.execute("INSERT INTO groups (name, password) VALUES (?, ?)", (group.name, group.password))
    group.id = cursor.lastrowid
    for user in group.users:
        cursor.execute("INSERT INTO users_groups (user_id, group_id) VALUES (?, ?)", (user.id, group.id))
    for activity in group.activities:
        cursor.execute("INSERT INTO activities (name, group_id) VALUES (?, ?)", (activity.name, group.id))

def insert_user_preference(user_preference):
    cursor.execute("INSERT INTO user_preferences (user_id, group_id, accommodation_preference, budget_preference, travel_style_preference) VALUES (?, ?, ?, ?, ?)", 
                   (user_preference.user.id, user_preference.group.id, user_preference.accommodation_preference, 
                    user_preference.budget_preference, user_preference.travel_style_preference))
    user_preference.id = cursor.lastrowid

# Create objects
user1 = User("John", "password1")
user2 = User("Jane", "password2")

group1 = Group("Group 1", "group1password")
group2 = Group("Group 2", "group2password")

activity1 = Activity("Activity 1")
activity2 = Activity("Activity 2")

accommodation1 = Accommodation("Accommodation 1")
accommodation2 = Accommodation("Accommodation 2")

preference1 = UserPreference(user1, group1, "Hotel", 100, "Luxury")
preference2 = UserPreference(user2, group1, "Apartment", 50, "Budget")

# Establish relationships
group1.users.append(user1)
group1.users.append(user2)
group1.activities.append(activity1)
group1.activities.append(activity2)
group1.accommodations.append(accommodation1)
group1.accommodations.append(accommodation2)

user1.preferences.append(preference1)
user2.preferences.append(preference2)

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

        name = request.form.get("group-name")
        pw = request.form.get("group-password")
        group = Group(name, pw)
        insert_group(group)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("group.html")

@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    return render_template("questionnaire.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        pw = request.form.get("password")
        user = User(username, pw)
        insert_user(user)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)