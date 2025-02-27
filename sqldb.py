import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import settings
from sqlalchemy import text
from string import ascii_letters
from random import choice
import sys

loginIdLen = 30

def connectDB():
    try:
        Database = mysql.connector.connect(
        host=getenv("DATABASE_HOST"),
        port=getenv("DATABASE_PORT"),
        user=getenv("DATABASE_USERNAME"),
        password=getenv("DATABASE_PASSWORD"),
        database=getenv("DATABASE")
        )
        print(Database)
        return Database
    except:
        print("Couldn't Connect to the Database")
        sys.exit()


    

def LoginUser(user, passw, session):
    Database = settings.Database
    query = "SELECT password FROM userdata WHERE username = %s"
    
    # Use parameterized queries to avoid SQL injection risks
    cursor = Database.cursor()
    cursor.execute(query, (user,))
    result = cursor.fetchone()[0] # Fetch the result
    print(result)
    if passw == result:
        loginid = LoginIdGen(Database)
        query = "INSERT INTO userdata (sessionid) VALUES (%s) WHERE username = %s"
        cursor.execute(query, (loginid, user,))
        Database.commit()

def LoginIdGen(Database):
    loginId = ""
    # Loop to get login id
    """ Login Id Generates an Id to use for verifying login. Everytime the page is refreshed the ID is checked against
    the database. If they do not match the user is logged out and the session is cleared. LoginID is checked against UserID which gives
    the user data to the site. This id must be generated everytime the user is logged in."""
    while True:
        for i in range(loginIdLen):
            loginId += choice(ascii_letters)
        query = "SELECT sessionid FROM userdata"
        for x in Database.cursor().execute(query).fetchall():
            if x == loginId:
                exists = True
                break
            else: 
                exists = False
        if not exists:
            break     
    return loginId
