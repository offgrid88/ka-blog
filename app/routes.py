#!/usr/bin/python

from flask import render_template, flash, redirect, url_for, request
from app import app
from dotenv import load_dotenv, find_dotenv
import urllib
import os
from pymongo import MongoClient



load_dotenv(find_dotenv())
password= urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))

username = urllib.parse.quote_plus(os.environ.get("USER_NAME"))


#app.config['SESSION_TYPE'] = 'memcached'
#app.config['SECRET_KEY'] = '1234'
#uri = "mongodb://{username}:{password}@127.0.0.1/offgrid8_db?authSource=offgrid8_db"
db= MongoClient('localhost', 27017, username=username, password=password,authSource="offgrid8_db")
#client = MongoClient(uri)
#
mydb=db.offgrid8_db
def databaseUsers():
    return mydb.users

def databaseArticles():
    return mydb.articles

usersDB = databaseUsers()
postsDB = databaseArticles()

"""def insert_doc():
    
    testdoc={
        "title":"test title",
        "content":"test content",
        "created_at":"20/02/2023",
        "author":"Aymen",
        "image":"urmm"
    }
    inserted_id=postsDB.insert_one(testdoc).inserted_id
    print(inserted_id)
insert_doc()"""

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

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_article', methods=["GET", "POST"])
def add_article():
    if request.method == "GET":
        return render_template("add_article.html")
    else:
        json = request.json
        print(json)     
        #with open("article", "w") as f:
        #    f.write()
        return render_template("add_article.html") 


@app.route('/read_article')
def read_article():
    with open("article", "r") as f:
        content = f.read()
    return render_template("articles.html",  posts= [content] ) 
