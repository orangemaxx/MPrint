from flask import Flask, render_template, request, redirect, session, url_for
from login import LoginAuth
import mysql.connector
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)


database = mysql.connector.connect(
    host=getenv("DATABASE"),
    user=getenv("DATABASE_USERNAME"),
    password=getenv("DATABASE_PASSWORD")
)
print(database)


# TODO: This is for testing purposes only. REMOVE THIS LATER!!!!
cursor = database.cursor()

cursor.execute("CREATE DATABASE maxsawesomedatabase")

cursor.execute("SHOW DATABASES")

for x in cursor:
    print(x)

# TODO: Make a config file. Ts dumb as hell.
app.secret_key = ["tjehjeflkjdjfkljIOjoifjdijfkfjKLJDKSJFUIOefhuei"]

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
        return render_template("index.html")
    else:
        pass

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