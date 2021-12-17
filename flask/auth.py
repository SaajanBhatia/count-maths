## Auth PY 
## Handles Login, Account Creation and Verification

## Import database functions
from sqlalchemy.orm import session
from db import database

from setup import getDb

# Password Hashing using SHA256_Crypt
from passlib.hash import sha256_crypt

class auth:
    def __init__(self, username, password, databaseConf):
        self.__username = username.upper()
        self.__password = password
        self.__database = database(
            host = databaseConf["HOST"],
            username = databaseConf["USERNAME"],
            password = databaseConf["PASSWORD"],
            database = databaseConf["DATABASE"],
            port = databaseConf["PORT"],
            db = getDb(databaseConf)
        )

    def getSessionDetails(self):
        return {
            "accountType" : "ADMIN",
            "email" : "Saajan@SSBhatia.co.uk",
            "firstName" : "Saajan",
            "lastName" : "Bhatia",
            "status" : "ACTIVE"
        }

    def returnMessage(self, type, message):
        return {
            "messageType":type,
            "message":message
        }

    def __validateUsername(self,username):
        allUsernames = self.__database.getAllUsernames()
        if (username,) in allUsernames:
            return True
        else:
            return False

    def __validatePassword(self,password):
        passwordHash = self.__database.getPasswordHash(self.__username)
        if sha256_crypt.verify(password,passwordHash):
            return True
        else:
            return False
        

    def createAccount(firstName, lastName, DOB, Address):
        ## Validate Username and Password
        ## Write to DB details
        pass

    def signIn(self):
        if self.__validateUsername(self.__username):
            if self.__validatePassword(self.__password):
                return self.returnMessage("SUCCESS", "Login Successful")
            else:
                return self.returnMessage("ERROR", "The Password is Incorrect.")
        else:
            return self.returnMessage("ERROR","The Account does not exist.")

    def getAccountsToModerate(self):
        pass



