#!/usr/bin/python
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from flask import render_template, flash, redirect, url_for, request, session,Flask,jsonify
from app import app
from dotenv import load_dotenv, find_dotenv
import os
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import datetime
import hashlib
import urllib




#######################################################
#           Mail config and functions                 #
#           Password generation using                 #
#        Minimalistic method via "bcrypt"             #
#######################################################


def send_mail():

    message="This passcode is available for 30 seconds, Time is of the essence,What ?!! you still reading !!... hurry up"
    smtp_server = "mail.aymenrachdi.xyz"
    port = 587  # For starttls
    sender_email = "contact@aymenrachdi.xyz"
    receiver_email = "contact@aymenrachdi.xyz"
    password = "Kernaug_758400"
    # Create a multipart message and set headers
    subject = "Offgrid request to post"
    body = "passcode ---->   <----" + message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message["Date"] = formatdate(localtime=True)

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        return message

######################################################


load_dotenv(find_dotenv())

password= urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))

username = urllib.parse.quote_plus(os.environ.get("USER_NAME"))




db= MongoClient('offgrid8_db', 27018, username=username, password=password,authSource="admin")
mydb=db.offgrid8_db
def databaseBooks():
    return mydb.books
    
def databaseArticles():
    return mydb.articles

booksDB = databaseBooks()
postsDB = databaseArticles()
users_collection = mydb["users"]

jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = '38dd56f56d405e02ec0ba4be4607eaab'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token


@app.route('/')
def index():
    return render_template('home.html')



@app.route('/articles')
def articles():
    allPosts = postsDB.find({})
    print(allPosts)
    return render_template('articles.html', posts = allPosts)



@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        allUsers = mydb.users.find({})
        userMails = [user["email"].lower() for user in allUsers]
        data = request.form
        email = data["email"]
        username = data["user"]
        psw = data["password"]
        verif = data["verif_pass"]
        new_user = {"email": email, "username": username, "password": psw}
        if psw != verif:
            error = "Password Mismatch !"
            return render_template('register.html', data=error)
        elif email.lower() in userMails:
            error = "Email address already exists !"
            return render_template('register.html', data=error)
        else:
            # Creating Hash of password to store in the database
            new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
            inserted_id=users_collection.insert_one(new_user)
            if inserted_id:
                return render_template('login.html', data=["green","Successfully Added, Please Log In"])
    else:
        return render_template('register.html')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login_details = request.form
#        email = data["email"]
#        psw = data["password"]
        allUsers = mydb.users.find({})
        # Checking if user exists in database or not
        user_from_db = users_collection.find_one({'username': login_details['username']})  # search for user in database
        # If user exists
        if user_from_db:
            # Check if password is correct
            encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
            if encrpted_password == user_from_db['password']:
                # Create JWT Access Token
                access_token = create_access_token(identity=user_from_db['username']) # create jwt token
                # Return Token
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({'msg': 'The username or password is incorrect'})
        
        for user in allUsers:
            if (user["email"] == email) and (user["password"] == psw):
                return render_template("add.html")
        return render_template('login.html', data=["red","Wrong Credentials !"])

    else:
        return render_template('login.html', data = ["",""])

@app.route('/books')
def books():
    allBooks = booksDB.find({})
    #print(allBooks)
    return render_template('books.html',books=allBooks)


@app.route('/fullpost', methods=['GET'])
def showFullPost():
    postId = request.args.get('postId')
    userPost = postsDB.find_one({'_id': ObjectId(postId)})
    return render_template('fullpost.html', post = userPost)

def getCurrentDateTime():
    currentDateTime = datetime.now()
    dt_string = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == "GET":
        return render_template("add_article.html")
    else:
        json = request.json
        inserted_id=postsDB.insert_one(json).inserted_id
        print("success")
        if inserted_id:
            print("success")
            return render_template('fullpost.html', post = inserted_id)
        else:
            print("failed")



