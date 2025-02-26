from flask import Flask, render_template, request, redirect, session, url_for
from login import LoginAuth

app = Flask(__name__)

app.secret_key = ["tjehjeflkjdjfkljIOjoifjdijfkfjKLJDKSJFUIOefhuei"]

@app.route("/", methods=["POST", "GET"])
def index():
    if session.get("logged_in"):
        return redirect(url_for('dash'))
    else:
        session.clear()
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Base login Page
        return render_template("index.html")
    else:
        pass

@app.route("/dashboard", methods=["GET"])
def dash():
    return("Hello")

app.run(debug=True)