""" MPrint - Written by Max Hewin
Follow me on letterboxd! https://letterboxd.com/orangemax
"""



from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from dotenv import load_dotenv
from os import getenv
from MPrint.sqldb import connectDB
from MPrint.loginmanager import LoginUser, checkLogin, Logout
# Settings is the global variables for this project. Anything that needs to be reused should be set in here
import MPrint.settings as settings
import MPrint.printjobmanager as printjobmanager

# Connect to The Mysql Database
Database = settings.Database = connectDB()

# TODO: Tomorow i would quite like to sort out the shitty organisation of ts project.
# The number of files is gradually increasing with every little bit that i add and so i would really really like to sort it out soonish
# This will make it hopefully easier to read so if i take a break i don't kms on return (previous instance: maxbox)

# TODO: Would be really super great to also document the database.
# Not much going on there rn but it is going to be absolutely atrocious pretty soon and i would like to make some rules that i can follow for editing the db.
# Hopefully this will also make it easier for other users

# TODO: also ideally gonna dick around with encryption tmr. would be nice to encrypt the passwords before shipping them off to the server.
# Just in case :)

# 28/02/2025
# - Max


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
        session.clear()
        # Base login Page
        # returns login html
        # TODO: Change to login.html or something not clapped
        return render_template("login.html", error=False)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        result = LoginUser(username, password)
        print(session.get('userId'))
        if result: return redirect(url_for('dash'))
        else: render_template("login.html", error=True)

# Basic log out system
# Use a form / button that posts to here then done easy peasy
# TODO: Add logout button on dash page
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if session.get("logged_in"):
        Logout()
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET"])
def dash():
    if not checkLogin(Database):
        return redirect(url_for('login'))
    # FIXME: okay so in an ideal world this should return true because ofc its gone thru to the database. but it aint and idk why. if anyone can fix this i would be very greatful
    print(printjobmanager.createPrintJob("yadayada", True, 1, 1))
    # Okay i dont really know where to go from here tbh at this point we gonna try work out how to make the dashboard but i hate html so i would rather go do smth else
    return str(session.get('userId'))



if __name__ == "__main__":
    app.run(debug=True)