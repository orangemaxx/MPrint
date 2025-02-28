import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import MPrint.settings as settings
from sqlalchemy import text
from string import ascii_letters
from random import choice
import sys
from flask import session

loginIdLen = 30


def LoginUser(user, passw):
    Database = settings.Database
    query = "SELECT password FROM userdata WHERE username = %s"
    
    # Use parameterized queries to avoid SQL injection risks
    cursor = Database.cursor()
    cursor.execute(query, (user,))
    result = cursor.fetchone()[0] # Fetch the result
    if passw == result:
        # Generate LoginId
        loginid = LoginIdGen(Database)
        # Set the update query for later use
        # Special thanks to 
        query = "UPDATE userdata SET sessionid = %s WHERE username = %s"
        # Fill in the values
        values = (loginid, user)
        # Execute the command
        cursor.execute(query, values)
        # Commit to DB
        Database.commit()
        session["loginId"] = loginid
        session["userId"] = getUserId(user, Database)
        session["logged_in"] = True
        return True
    else: return False

def LoginIdGen(Database):
    # Loop to get login id
    """ Login Id Generates an Id to use for verifying login. Everytime the page is refreshed the ID is checked against
    the database. If they do not match the user is logged out and the session is cleared. LoginID is checked against UserID which gives
    the user data to the site. This id must be generated everytime the user is logged in."""
    while True:
        exists = None
        loginId = ""
        # Generate the Login id
        for i in range(loginIdLen):
            loginId += choice(ascii_letters)
        # Check Unique
        cursor = Database.cursor()
        query = "SELECT sessionid FROM userdata"
        cursor.execute(query)
        result = cursor.fetchall()
        for x in result:
            if x == loginId:
                exists = True
                break
            else: 
                exists = False
        if not exists:
            break     
    return loginId

def getUserId(user, Database):
    query = "SELECT userid FROM userdata WHERE username = %s"
    mycursor = Database.cursor()
    mycursor.execute(query, (user,))
    result = mycursor.fetchone()[0]
    print(result)
    return result


def Logout():
    userid = session.get("userId")
    loginid = session.get("loginId")
    Database = settings.Database
    if checkLogin(Database):
        query = "UPDATE userdata SET sessionid = NULL WHERE userid = %s"
        cursor = Database.cursor()
        cursor.execute(query, (userid,))
        Database.commit()
        return True
    else: return False


def checkLogin(Database):
    # try:
        userid = session.get("userId")
        loginid = session.get("loginId")
        query = "SELECT sessionid FROM userdata WHERE userid = %s"
        cursor = Database.cursor()
        cursor.execute(query, (userid,))
        result = cursor.fetchone()[0]
        if result == loginid:
            return True
        else: return False
    # except:
    #     print("Couldn't Get Session")
    #     return False