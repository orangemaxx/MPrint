# Used for managing adding and retriving print jobs
import MPrint.settings as settings
from string import ascii_letters
from flask import session
from random import choice

import MPrint.sqldb as sqldb
import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()

jobidlen = 45
Database = settings.Database()

def createPrintJob(file):
    session.get("userId")
    if not sqldb.checkLogin(Database):
        return False
    jobId = createJobId()


def createJobId():
    while True:
        jobId = ""
        for x in range(jobidlen):
            jobId += choice(ascii_letters)
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

