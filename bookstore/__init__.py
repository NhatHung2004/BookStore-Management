from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://NhatHung:nhathung123@localhost/storedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = 'HGHJAHA^&^&*AJAVAHJ*^&^&*%&*^GAFGFAG'

db = SQLAlchemy(app)
login = LoginManager(app)
admin = Admin(app, name="Book Store", template_mode="bootstrap3")
app.config["PAGE_SIZE"] = 4

cloudinary.config(
    cloud_name="dvahhupo0",
    api_key="461556863519315",
    api_secret="lBLWun6CURjcaUNB8G7qUQtHtxo",  # Click 'View API Keys' above to copy your API secret
    secure=True
)
