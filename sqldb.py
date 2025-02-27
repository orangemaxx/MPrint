import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import settings



def connectDB():
    Database = mysql.connector.connect(
    host=getenv("DATABASE"),
    port=getenv("DATABASE_PORT"),
    user=getenv("DATABASE_USERNAME"),
    password=getenv("DATABASE_PASSWORD")
    )

    return Database

def testSettings():
    print("test")
    print(settings.Database)