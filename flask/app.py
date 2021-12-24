''' 
    Count on us Mathematics
'''

import logging
from re import template
from flask import Flask, session, redirect
import secrets

## Import the Database Config
from setup import databaseConfig

## Import Auth 
from auth import auth

## Configure Logging
logging.basicConfig(
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S',
    filename='./error.log', 
    filemode='w'
)

## App Declaration
app = Flask(__name__)

# Set Session
def setSession(details):
    details = list(details[0])
    session["userDetails"] = details

## Hope
@app.route("/")
def home():
    if session:
        return str(session["userDetails"])
    else:
        return '''
            <h1 style="color:red">Home Blog Page</h1>
            <p>Not Signed In</p>
        '''

# About (Static Page)
@app.route("/about")
def about():
    return '''
        <h1>About Page</h1>
    '''

# Sign In Route
@app.route("/signIn")
def signIn():
    # sample data
    username = "SaajanBhatia"
    password = ""

    user = auth(username, password, databaseConfig)
    token = user.signIn()
    if token["messageType"] == "SUCCESS":
        setSession(user.getSessionDetails())
    return (str(token) + str(session["userDetails"]))

# Sign Out Route
@app.route("/signOut")
def signOut():
    session.clear()
    return redirect("/")

# Create Account Route
@app.route("/createAccount")
def createAccount():
    ## Ex data
    username = "johny"
    password = "Psdf"
    fName = "John"
    lName = "Doe"
    homeAddr = "E11 1JX"
    email = "john@gmail.com"
    dateOfBirth = "14/03/2000"

    tempUser = auth(username, password, databaseConfig,)
    token = tempUser.createAccount(homeAddr=homeAddr, email=email, dob=dateOfBirth, firstName=fName, lastName=lName)
    return ("CREATE ACCOUNT: \n" + str(token))

if __name__ == "__main__":
    logging.warning("SERVER STARTED")
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.run(
        debug = True,
        host = 'localhost',
        port = 5000
    )