import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import settings




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
    # Database = settings.Database
    # query = "SELECT * FROM users WHERE username = :user"
    # mycursor = Database.cursor()
    # mycursor.execute(query,{"user":user}).fetchone()
    # print(mycursor)
    Database = settings.Database
    query = text("SELECT * FROM userdata ")