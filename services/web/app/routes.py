#!/usr/bin/python

from flask_mail import Mail, Message
from flask import render_template, flash, redirect, url_for, request, session,Flask
from app import app
from dotenv import load_dotenv, find_dotenv
import urllib
import os
from bson import ObjectId
from datetime import datetime
from flask import Flask
from pymongo import MongoClient
import pymongo
import bcrypt
import datetime
import hashlib
import urllib


######################################################
#                                                     #
#                                                     #
#           Mail config and functions                 #
#                                                     #
#                                                     #
#                                                     #
#                                                     #
######################################################
app.config['MAIL_SERVER']='mail.aymenrachdi.xyz'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'contact@aymenrachdi.xyz'
app.config['MAIL_PASSWORD'] = 'Kernaug_758400'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
######################################################

app.secret_key = "testing"
load_dotenv(find_dotenv())

password= urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))

username = urllib.parse.quote_plus(os.environ.get("USER_NAME"))
print(password,username)
db= MongoClient('offgrid8_db', 27018, username=username, password=password,authSource="admin")
mydb=db.offgrid8_db
def databaseBooks():
    return mydb.books

def generate_password():
    password=""
    return password

def password_to_mail():
   msg = Message('Offgrid request to post', sender = 'contact@aymenrachdi.xyz', recipients = ['contact@aymenrachdi.xyz'])
   msg.body = "This passcode is available for 30 seconds, Time is of the essence, you still reading !!... hurry up "
   mail.send(msg)
   return "Sent"



def is_user_valid(passwd):
    aymen_password="Kernel_Augmentation758400"
    if passwd==aymen_password:
        return True
    else:
        return False
    
def databaseArticles():
    return mydb.articles

booksDB = databaseBooks()
postsDB = databaseArticles()

@app.route('/')
def index():

    #allPosts = articles.find({})
    return render_template('home.html')



@app.route('/articles')
def articles():
    allPosts = postsDB.find({})
    print(allPosts)
    return render_template('articles.html', posts = allPosts)

@app.route('/getpass' ,methods=['POST'])
def getpass():
    if request.method == 'POST':
        if request.form['submit_button'] == 'get pass':
            pass
            print("email_sent")

@app.route('/books' ,methods=['GET', 'POST'])
def books():
    if request.method == "POST":
        info = request.form['info']
        thoughts = request.form['thoughts']
        password = request.form['password']
        json={"info":info,"thoughts":thoughts}
        if is_user_valid(password):
            inserted_id=booksDB.insert_one(json).inserted_id
            if inserted_id:
                print("success")
            return render_template('books.html', books = inserted_id)
            #return f'{info}, {thoughts},{password}'
        else:
            return render_template('invalid.html',error=error)
    else:
        allBooks = booksDB.find({})
        print(allBooks)
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



@app.route('/add_article', methods=["GET", "POST"])
def add_article():
    
    if request.method == "GET":
        return render_template("add_article.html")
    else:
        #password = request.form['password']
        
        json = request.json
        password=json["password"]
        json.pop("password")
        print(json)
        #print(password)
        if is_user_valid(password):
            inserted_id=postsDB.insert_one(json).inserted_id
            if inserted_id:
                print("success")
            return render_template('fullpost.html', post = inserted_id)

