#!/usr/bin/python
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from flask import Flask, render_template, flash, redirect, url_for, request, session
from app import app
from dotenv import load_dotenv, find_dotenv
import os
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
import datetime
import bcrypt, hashlib
import urllib
from flask_login import LoginManager ,login_user,login_required,logout_user,current_user,UserMixin


#######################################################
#           Mail config and functions                 #
#           Password generation using                 #
#        Minimalistic method via "bcrypt"             #
#######################################################


def send_mail():

    message="This passcode is available for 30 seconds, Time is of the essence,What ?!! you still reading !!... hurry up"
    smtp_server = "mail.aymenrachdi.xyz"
    port = 587  # For starttls
    sender_email = ""
    receiver_email = ""
    password = ""
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

app.secret_key = 'dfdfdsfslvksfùvvùlsfvl;fsùv;ùfsv'
app.config['SESSION_TYPE'] = 'filesystem'


db= MongoClient('offgrid8_db', 27018, username=username, password=password,authSource="admin")
mydb=db.offgrid8_db
def databaseBooks():
    return mydb.books
    
def databaseArticles():
    return mydb.articles

booksDB = databaseBooks()
postsDB = databaseArticles()
users_collection = mydb["users"]


@app.route("/register", methods=['post', 'get'])
def register():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("add"))
    if request.method == "POST":
        username = request.form.get("user")
        email = request.form.get("email")
        password = request.form.get("password")
        psw = request.form.get("verif_pass")
        #if found in database showcase that it's found 
        username_found = users_collection.find_one({"name": username})
        email_found = users_collection.find_one({"email": email})
        if username_found:
            message = 'There already is a username by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password != psw:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(psw.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            username_input = {'name': username, 'email': email, 'password': hashed}
            #insert it in the record collection
            users_collection.insert_one(username_input)
            
            #find the new created account and its email
            username_data = users_collection.find_one({"email": email})
            new_email = username_data['email']
            #if registered redirect to logged in as the registered username
            return render_template('add.html', email=new_email)
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("add"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #check if email exists in database
        email_found = users_collection.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encoded_passwordcheck=passwordcheck.encode('utf-8')
            hashed_passwordcheck=bcrypt.hashpw(passwordcheck, bcrypt.gensalt())
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), hashed_passwordcheck):
                session["email"] = email_val
                return redirect(url_for('add'))
            else:
                if "email" in session:
                    return redirect(url_for("add"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)



@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')
    



@app.route('/')
def index():
    return render_template('home.html')



@app.route('/articles')
def articles():
    allPosts = postsDB.find({})
    print(allPosts)
    return render_template('articles.html', posts = allPosts)


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
    if "email" in session:
        email = session["email"]
        if request.method == "GET":
            return render_template('add.html', email=email)
        else:
            json = request.json
            inserted_id=postsDB.insert_one(json).inserted_id
            print("success")
            if inserted_id:
                print("success")
                return render_template('fullpost.html', post = inserted_id)
            else:
                print("failed")
    else:
        return redirect(url_for("login"))



