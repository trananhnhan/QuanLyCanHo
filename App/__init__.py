from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/canhodb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login =LoginManager(app)