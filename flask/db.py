## DB PY Functions for Reading and Writing to Database

## Import Datetime Module
import datetime

class database:
    ## Database details
    def __init__(self, host, username, password, database, port, db):
        self.host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__port = port
        self.__db = db
    
    def getAllUsernames(self):
        allUsernames = self.__db.execute(
            "SELECT username FROM count_maths.member_details;"
        ).fetchall()
        return allUsernames

    def getPasswordHash(self, username):
        passwordHash = self.__db.execute(
            "select password from member_details where member_details.username = :username ", {
                "username" : username
            }
        ).fetchone()
        return passwordHash[0]

    def getUserDetails(self, username):
        userDetails = self.__db.execute(
            "SELECT accountType, email, firstName, lastName, status, homeAddress, dateOfBirth from member_details where member_details.username = :username", {
                "username" : username
            }
        ).fetchall()
        return userDetails

    def getUserID(username):
        pass

    def addNewMember(self, userInfo):
        self.__db.execute(
            "INSERT INTO member_details(username,password,firstName,lastName,homeAddress,dateOfBirth,status,email,dateCreated,accountType) VALUES \
                (:username,:password,:firstName,:lastName,:homeAddress,:dateOfBirth,:status,:email,:dateCreated,:accountType)",
                {
                    "username" : userInfo["username"],
                    "password" : userInfo["password"],
                    "firstName" : userInfo["firstName"],
                    "lastName" : userInfo["lastName"],
                    "homeAddress" : userInfo["homeAddr"],
                    "dateOfBirth" : userInfo["dob"],
                    "status" : "MODERATE",
                    "email" : userInfo["email"],
                    "dateCreated" : (datetime.datetime.now().strftime("%Y/%m/%d")),
                    "accountType" : "STUDENT"
                }
        )
        
        self.__db.commit()

    
    def updateMember():
        pass

    def setMemberActive():
        pass

    def setMemberInactive():
        pass

    
