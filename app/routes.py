#!/usr/bin/python
from flask import render_template, flash, redirect, url_for
from app import app



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



