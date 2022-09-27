#!/usr/bin/python
from app import app
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate





#app.config.from_object(Config)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add_article')
def add_article():
    return render_template('add_article.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')



