from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from dotenv import load_dotenv
from os import getenv
from sqldb import connectDB, LoginUser
# Settings is the global variables for this project. Anything that needs to be reused should be set in here
import settings

Database = settings.Database = connectDB()
print(settings.Database)


app = Flask(__name__)
app.secret_key = getenv("SESSION_SECRET")



@app.route("/", methods=["POST", "GET"])
def index():
    if session.get("logged_in"):
        return redirect(url_for('dash'))
    else:
        session.clear()
        return redirect(url_for('login'))

# Login page here
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Base login Page
        # returns login html
        # TODO: Change to login.html or something not clapped
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        LoginUser(username, password, session)
        return "1"

# Basic log out system
# Use a form / button that posts to here then done easy peasy
# TODO: Add logout button on dash page
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET"])
def dash():
    return("Hello")

app.run(debug=True)