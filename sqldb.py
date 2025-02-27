import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import settings
from sqlalchemy import text
from string import ascii_letters
from random import choice

loginIdLen = 30

def connectDB():
    Database = mysql.connector.connect(
    host=getenv("DATABASE_HOST"),
    port=getenv("DATABASE_PORT"),
    user=getenv("DATABASE_USERNAME"),
    password=getenv("DATABASE_PASSWORD"),
    database=getenv("DATABASE")
    )

    return Database

def LoginUser(user, passw, session):
    Database = settings.Database
    query = "SELECT password FROM userdata WHERE username = %s"
    
    # Use parameterized queries to avoid SQL injection risks
    cursor = Database.cursor()
    cursor.execute(query, (user,))
    result = cursor.fetchone()[0] # Fetch the result
    print(result)
    if passw == result:
        
        query = "INSERT INTO userdata (sessionid) VALUES (%s) WHERE username = %s"
        cursor.execute(query, (LoginIdGen(Database), user))
        Database.commit()

def LoginIdGen(Database):
    loginId = ""
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