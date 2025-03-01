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

    # TODO: PLEASE NOTE SO FAR TS DOES NOT SAVE THE FILE. ONLY DATABASE STUFF SO FAR. UNDECIDED IF I WANT TO SAVE THE FILE HERE OR SOMEWHERE ELSE. MIGHT BE EASIER TO HAVE IT ALL CENTRALISED

    # IMPORTANT NOTE: Earlier today there was a stupid fucking issue that occoured here in this very function that would crash the whole damn server
    # I fixed the issue in commit b6d3eed => https://github.com/orangemaxx/MPrint/commit/b6d3eed99f9bef301231b0e7b8923682b42b9d4d
    # Now the issue with this is that i have utterly NO CLUE how it got fixed.
    # if anyone would be so kind as to read thru this code and report below on WHAT i did to fix this issue i would geniuenly appreciate it so so so much
    # ts nearly killed me and the project so if it happens again idk what im gonna do (prolly read thru the commit)
    # thanks in advance - max

    # Hi my name is _____ and the way it was fixed was by: (put explaination here)

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

def getJobExpiry(): # this func gets 12 hours after the job creation so it can expire and whatnot
    time = datetime.now()
    expiry = time + timedelta(hours=12) # adds 12 hours
    return int(expiry.timestamp()) # converts to int and to unix time. doesn't need to be super accurate

def clearJobs():
    # TODO: Write code to delete files from server that corospond to ts jobid
    Database = settings.Database # Set database
    time = int(datetime.now().timestamp()) # get the current time

    cursor = Database.cursor() # Set cursor
    query = "SELECT jobid FROM printjobs WHERE jobexpirytime >= %s"
    values = (time,) # read the code
    cursor.execute(query, values) # read the code
    result = cursor.fetchall()
    for x in result:
        idcursor = Database.cursor() # idk if you have to reset the cursor everytime however i spent 4 hours fixing cursor bullshit this morning so we doing it anyways.
        query = "DELETE FROM printjobs WHERE jobid = %s" # Where id = the id we've selected DELETE!!!
        values = (x,) # set the values as the dang for x loop thing
        idcursor.executemany(query, values) # you know how it is
    Database.commit() # commit things to the database. might move this up cuz if one thing goes wrong atp we cooked but idk