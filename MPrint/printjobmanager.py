# Used for managing adding and retriving print jobs
import MPrint.settings as settings
from MPrint.loginmanager import checkLogin
from string import ascii_letters
from flask import session
from random import choice
from datetime import datetime, timedelta

import MPrint.sqldb as sqldb
import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()

jobidlen = 30

def createPrintJob(filename, color, pages, copies):

    # TODO: ALMOST FORGOT TO ADD JOB EXPIRRY DO THAT SOON!!! Gotta be able to delete the files because we are not doing allat.
    # TODO: ALSO PLEASE NOTE SO FAR TS DOES NOT SAVE THE FILE. ONLY DATABASE STUFF SO FAR. UNDECIDED IF I WANT TO SAVE THE FILE HERE OR SOMEWHERE ELSE. MIGHT BE EASIER TO HAVE IT ALL CENTRALISED

    Database = settings.Database
    if not checkLogin(Database):
        return False
    # Create the job id
    jobId = createJobId(Database)
    # Get the userid
    userid = session.get("userId")
    # Get the job expiry time
    expiry = getJobExpiry()
    # Set the cursor for query
    mycursor = Database.cursor() # <- this is where the error keeps appearing. Please note there is error prevention in place. If we can't connect to the database the app will not run.
    # Set the query for mysql
    query = "INSERT INTO printjobs (jobid, userid, jobfilename, jobscolour, pages, copies, jobexpirytime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # Set the variables
    val = (jobId, userid, filename, color, pages, copies, expiry)
    print("yeah") # TODO: This is to check it got this far. Get rid of this later
    mycursor.execute(query, val) # Execute command in mysql database
    Database.commit() # commit to database
    return True # return true if succesful


def createJobId(Database):
    exists = None
    while True:
        jobId = ""
        # Randomly create jobid
        for i in range(jobidlen):
            jobId += choice(ascii_letters)
        # Check against database
        cursor = Database.cursor()
        query = "SELECT jobid FROM printjobs"
        cursor.execute(query)
        result = cursor.fetchall()
        for x in result:
            if x == jobId:
                exists = True
                break
            else:
                exists = False
        if not exists: break
    return jobId

def getJobExpiry():
    time = datetime.now()
    expiry = time + timedelta(hours=12)
    return int(expiry.timestamp())

def clearJobs():
    Database = settings.Database
    time = int(datetime.now().timestamp())

    cursor = Database.cursor()
    query = "SELECT jobid FROM printjobs WHERE jobexpirytime >= %s"
    values = (time,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    for x in result:
        idcursor = Database.cursor()
        query = "DELETE FROM printjobs WHERE jobid = %s"
        idcursor.executemany(query, (x,))
    Database.commit()