''' 
    Count on us Mathematics
'''

import logging
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
    session["userDetails"] = details

## Hope
@app.route("/")
def home():
    return '''
        <h1>Home Blog Page</h1>
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
    return ( "Sign IN" + str(session["userDetails"]) )
    

@app.route("/signOut")
def signOut():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    logging.warning("SERVER STARTED")
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.run(
        debug = True,
        host = 'localhost',
        port = 5000
    )