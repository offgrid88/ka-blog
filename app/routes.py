#!/usr/bin/python

from flask import render_template, flash, redirect, url_for, request
from app import app
from dotenv import load_dotenv, find_dotenv
import urllib
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from flask import Flask
from pymongo import MongoClient
import hashlib
from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

import datetime
import hashlib
import urllib



app.secret_key = "testing"
load_dotenv(find_dotenv())

password= urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))

username = urllib.parse.quote_plus(os.environ.get("USER_NAME"))

db= MongoClient('localhost', 27017, username=username, password=password,authSource="offgrid8_db")
mydb=db.offgrid8_db
def databaseUsers():
    return mydb.users

def databaseArticles():
    return mydb.articles

usersDB = databaseUsers()
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

@app.route('/fullpost', methods=['GET'])
def showFullPost():
    postId = request.args.get('postId')
    userPost = postsDB.find_one({'_id': ObjectId(postId)})
    return render_template('fullpost.html', post = userPost)

def getCurrentDateTime():
    currentDateTime = datetime.now()
    dt_string = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

#Write Post

"""@app.route('/writepost', methods=['GET', 'POST'])
def writePost():

    if 'name' not in session:
        return redirect('/login')

    else:
        userProfile = usersDB.find_one({'username': session['username']})
        if request.method == 'POST':
            postInsert = postsDB.insert_one( { 'username': session['username'], 
                'created_at': getCurrentDateTime(), 'updated_at': None, 'title': request.form['title'],
                'content': request.form['content'], 'image': request.form['image']} )
            flash('Post Submitted Successfully')
            return redirect('/')
        else:
            return render_template('writepost.html', userProfile = userProfile)
"""


@app.route('/about')
def about():
    return render_template('about.html')

def is_user_valid(user,passwd):
    aymen_username="mdx8"
    aymen_password="Kernel_Augmentation758400"
    if user==aymen_username and passwd==aymen_password:
        return True
    else:
        return False

@app.route('/add_article', methods=["GET", "POST"])
def add_article():

    if request.method == "GET":
        return render_template("add_article.html")
    else:
        json = request.json
        print(json)
        #if is_user_valid()
        inserted_id=postsDB.insert_one(json).inserted_id
        print(inserted_id)
        return render_template('fullpost.html', post = inserted_id)

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)