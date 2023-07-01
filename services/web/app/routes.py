#!/usr/bin/python
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from flask import render_template, flash, redirect, url_for, request, session,Flask
from app import app
from dotenv import load_dotenv, find_dotenv
import urllib
import os
from bson import ObjectId
from datetime import datetime
from flask import Flask
from pymongo import MongoClient
import bcrypt
import datetime
import hashlib
import urllib




#######################################################
#           Mail config and functions                 #
#           Password generation using                 #
#        Minimalistic method via "bcrypt"             #
#######################################################


def password_to_mail():

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

#app.secret_key = "testing"
load_dotenv(find_dotenv())

password= urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))

username = urllib.parse.quote_plus(os.environ.get("USER_NAME"))
print(password,username)
db= MongoClient('offgrid8_db', 27018, username=username, password=password,authSource="admin")
mydb=db.offgrid8_db
def databaseBooks():
    return mydb.books




    
def databaseArticles():
    return mydb.articles

booksDB = databaseBooks()
postsDB = databaseArticles()

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
        json = {"email": email, "username": username, "password": psw}
        if psw != verif:
            error = "Password Mismatch !"
            return render_template('register.html', data=error)
        elif email.lower() in userMails:
            error = "Email address already exists !"
            return render_template('register.html', data=error)
        else:
            inserted_id = mydb.users.insert_one(json).inserted_id
            if inserted_id:
                return render_template('login.html', data=["green","Successfully Added, Please Log In"])
    else:
        return render_template('register.html')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        psw = data["password"]
        allUsers = mydb.users.find({})
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

@app.route('/add')
def add():
    return render_template("add.html")



