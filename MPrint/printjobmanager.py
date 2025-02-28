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
    # FIXME: AttributeError: 'NoneType' object has no attribute 'cursor'
    # https://paste.mozilla.org/60K3T2kj

    # TODO: ALMOST FORGOT TO ADD JOB EXPIRRY DO THAT SOON!!! Gotta be able to delete the files because we are not doing allat.
    # TODO: ALSO PLEASE NOTE SO FAR TS DOES NOT SAVE THE FILE. ONLY DATABASE STUFF SO FAR. UNDECIDED IF I WANT TO SAVE THE FILE HERE OR SOMEWHERE ELSE. MIGHT BE EASIER TO HAVE IT ALL CENTRALISED

    # TODO: Hoping clyde can debug this
    Database = settings.Database
    if not checkLogin(Database):
        return False
    print(Database) # TODO: Testing purposes. Get rid of this later
    # Set the cursor for query
    mycursor = Database.cursor() # <- this is where the error keeps appearing. Please note there is error prevention in place. If we can't connect to the database the app will not run.
    # Create the job id
    jobId = createJobId()
    # Get the userid
    userid = session.get("userId")
    # Set the query for mysql
    query = "INSERT INTO printjobs (jobid, userid, jobfilename, jobscolour, pages, copies) VALUES (%s, %s, %s, %s, %s, %s)"
    # Set the variables
    val = (jobId, userid, filename, color, pages, copies)
    print("yeah") # TODO: This is to check it got this far. Get rid of this later
    mycursor.execute(query, val) # Execute command in mysql database
    Database.commit() # commit to database
    return True # return true if succesful


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

