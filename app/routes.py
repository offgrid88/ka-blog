#!/usr/bin/python
from flask import render_template, flash, redirect, url_for
from app import app
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os 
import pprint
import urllib

load_dotenv(find_dotenv())
password= urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
#username=os.environ.get("USER_NAME")
username = urllib.parse.quote_plus(os.environ.get("USER_NAME"))
#password = urllib.parse.quote_plus(password)

#app.config['SESSION_TYPE'] = 'memcached'
#app.config['SECRET_KEY'] = '1234'
#uri = "mongodb://{username}:{password}@127.0.0.1/offgrid8_db?authSource=offgrid8_db"
client= MongoClient('localhost', 27017, username=username, password=password,authSource="offgrid8_db")
#client = MongoClient(uri)
#
dbs=client.list_database_names()
db=client.offgrid8_db
collections=db.list_collection_names()
print(dbs,collections)
collection=db.articles
def insert_doc():
    
    testdoc={
        "title":"test title",
        "content":"test content",
        "created_at":"20/02/2023",
        "author":"Aymen",
        "image":"urmm"
    }
    inserted_id=collection.insert_one(testdoc).inserted_id
    print(inserted_id)
insert_doc()
#def databasePosts():
#    return MongoClient('127.0.0.1:27017').rudr.posts

@app.route('/')
def index():

    allPosts = collection.find({})
    return render_template('home.html')

#Write Post
@app.route('/writepost', methods=['GET', 'POST'])
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

def getCurrentDateTime():
    currentDateTime = datetime.now()
    dt_string = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

@app.route('/add_article')
def add_article():
    return render_template('add_article.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    allPosts = collection.find({})
    print(allPosts)
    return render_template('articles.html', posts = allPosts)

@app.route('/projects')
def projects():
    return render_template('projects.html')



