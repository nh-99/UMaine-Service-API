from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
databasePassword = os.environ['DB_PASSWORD']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:{}@umaineserviceapi_mysql_1/umaine_users'.format(databasePassword)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:{}@localhost/umaine_users'.format(databasePassword)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(254), unique=True)
    serviceKeys = db.Column(db.String(3072), unique=True, nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
