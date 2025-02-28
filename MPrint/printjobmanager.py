# Used for managing adding and retriving print jobs
import MPrint.settings as settings
from MPrint.loginmanager import checkLogin
from string import ascii_letters
from flask import session
from random import choice

import MPrint.sqldb as sqldb
import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()

jobidlen = 45
Database = settings.Database

def createPrintJob(filename, color, pages, copies):
    
    if not checkLogin(Database):
        return False
    jobId = createJobId()
    userid = session.get("userId")

    query = "INSERT INTO printjobs (jobid, userid, jobfilename, jobscolour, pages, copies) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (jobId, userid, filename, color, pages, copies)
    cursor = Database.cursor()
    print("yeah")
    cursor.execute(query, val)
    Database.commit()
    return True


def createJobId():
    while True:
        jobId = ""
        # Randomly create jobid
        for x in range(jobidlen):
            jobId += choice(ascii_letters)
        # Check against database
        cursor = Database.cursor()
        query = "SELECT jobid FROM printjobs"
        result = cursor.execute(query).fetchall()
        for x in result:
            if x == jobId:
                exists = True
                break
            else:
                exists = False
        if not exists:
            break
        else: continue
    return jobId

