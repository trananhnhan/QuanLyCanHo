from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)

app.secret_key = "finieninfien"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/canhodb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
cloudinary.config(cloud_name='dddesdoxw',
                  api_key='951846773826526',
                  api_secret='ac1UUbrVhdWPE8vtYAfdC2-Co8Y')

db = SQLAlchemy(app)
login =LoginManager(app)