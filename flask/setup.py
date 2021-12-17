from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

# Password Hashing using SHA256_Crypt
from passlib.hash import sha256_crypt

import logging

from sqlalchemy.sql.expression import false
from getpass import getpass

## Configure Logging
import logging
logging.basicConfig(
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S',
)

## Only Supports MySQL
databaseConfig = {
    "HOST" : "localhost",
    "PORT" : "3306",
    "USERNAME" : "root",
    "PASSWORD" : "Password_123",
    "DATABASE" : "COUNT_MATHS",
    "SERVICE" : "MYSQL",
    "CONNECTION" : "localhost via TCP/IP"
}

'''
    Account Types : [Student, Tutor, Admin]
'''

membersTable = (
    "CREATE TABLE member_details ( \
    memberID INT AUTO_INCREMENT PRIMARY KEY, \
    username CHAR(200) NOT NULL, \
    password MEDIUMTEXT, \
    firstName CHAR(200), \
    lastName CHAR(200), \
    homeAddress MEDIUMTEXT, \
    dateOfBirth DATE, \
    status CHAR(100), \
    email CHAR(200), \
    accountType CHAR(100) NOT NULL);"
)



def getDb(databaseConfig):
    engine = create_engine("mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(
            password = databaseConfig["PASSWORD"],
            database = databaseConfig["DATABASE"],
            username = databaseConfig["USERNAME"],
            host = databaseConfig["HOST"],
            port = databaseConfig["PORT"]
        ))
    db = scoped_session(sessionmaker(bind=engine))
    return db

def __errorHandler(type, message):
    if type == "ERROR":
        logging.error(message)
    else:
        logging.warning(message)

def logMessage(message):
    print ("--> " + message)

def checkDatabaseConfig():
    valid = True
    for key in databaseConfig.keys():
        if databaseConfig[key] == "":
            valid = False
    return valid

def createTables(db):
    db.execute(membersTable)
    logMessage("Members Table Created")
    db.commit()

def getAdminDetails():
    logMessage("Admin Account Configuration")
    username = str(input("Enter Admin Username: \n"))
    password = getpass("Enter Admin Password: ")
    fName = str(input("Enter First Name: \n"))
    lName = str(input("Enter Last Name: \n"))
    return {
        "username" : username.upper(),
        "password" : sha256_crypt.hash(password),
        "fName" : fName,
        "lName" : lName
    }


def addAdminToDb(details, db):
    db.execute("INSERT INTO member_details(username, firstName, lastName, password, accountType, status) \
        VALUES(:username, :firstName, :lastName, :password, :accountType, :status)",{
            "username" : details["username"],
            "firstName" : details["fName"],
            "lastName" : details["lName"],
            "password" : details["password"],
            "accountType" : "ADMIN",
            "status" : "ACTIVE"
        })
    db.commit()

def setUpDb():
    logMessage("STARTING DATABASE SETUP")
    if checkDatabaseConfig():
        db = getDb(databaseConfig)
        try:
            allTables = db.execute("SHOW TABLES;").fetchall()
        except sqlalchemy.exc.OperationalError as err:
            __errorHandler("ERROR", "sqlalchemy.exc.OperationalError, please check setup configuration")
            return False
        else:
            allTables = db.execute("SHOW TABLES;").fetchall()
            if allTables == []:
                createTables(db)
                addAdminToDb(getAdminDetails(), db)

            else:
                __errorHandler("ERROR", "Please ensure database is empty")
                return False
            
        
        

    else:
        __errorHandler("ERROR", "Please complete database configuration first.")
        return False
