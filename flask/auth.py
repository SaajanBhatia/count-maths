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
        userDetails = self.__database.getUserDetails(self.__username)
        return userDetails

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

    def validPasswordStrength(self, password):
        if len(password) < 6:
            return [False, "Password is too short."]

        if len(password) > 50:
            return [False, "Password is too long."]

        if not any(char.isdigit() for char in password):
            return [False, "Password must contain a number."]

        if not any(char.isupper() for char in password):
            return [False, "Password should have at least one uppercase letter."]
          
        if not any(char.islower() for char in password):
            return [False, "Password should have at least one lowercase letter."]
       
        return [True]
        

    def createAccount(self, homeAddr, email, dob, firstName, lastName):
        ## Validate Username 
        usernames = self.__database.getAllUsernames()
        if (self.__username,) in usernames:
            return self.returnMessage("ERROR", "Username already exists.")

        ## Validate Password
        validPswrd = self.validPasswordStrength(self.__password)
        if not validPswrd[0]:
            return self.returnMessage("ERROR", validPswrd[1])

        ## Write to DB details
        # Put info into PY DICT
        userInfo = {
            "homeAddr" : homeAddr,
            "email" : email,
            "dob" : dob,
            "firstName" : firstName,
            "lastName" : lastName,
            "username" : self.__username,
            "password" : sha256_crypt.encrypt(self.__password)
        }

        self.__database.addNewMember(userInfo)

        ## Return success
        return self.returnMessage("SUCCESS", "Account Created")

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



