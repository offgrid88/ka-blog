from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mdx8:I.lovecpu758400@localhost/low-life'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models


