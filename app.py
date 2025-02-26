from flask import Flask, render_template, request, redirect, session, url_for
from login import LoginAuth

app = Flask(__name__)

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
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET"])
def dash():
    return("Hello")

app.run(debug=True)