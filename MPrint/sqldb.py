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

def connectDB():
    try:
        Database = settings.Database = mysql.connector.connect(
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


    


