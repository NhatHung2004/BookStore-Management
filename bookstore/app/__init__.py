from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from vnpay import VNPay
from flask_mail import Mail
import os


app = Flask(__name__)
app.secret_key = 'HGHJAHA^&^&*AJAVAHJ*^&^&*%&*^GAFGFAG'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.environ.get('MYSQL_USERNAME')}:{os.environ.get('MYSQL_PASSWORD')}@localhost/storedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8
app.config["PAGE_MANAGE"] = 4
# Cấu hình email server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')


db = SQLAlchemy(app)
login = LoginManager(app)
mail = Mail(app)


cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET'),
    secure=True
)


VNP_TMN_CODE = os.environ.get('VNP_TMN_CODE')
VNP_HASH_SECRET = os.environ.get('VNP_HASH_SECRET')
VNP_URL = os.environ.get('VNP_URL')

vnpay = VNPay(VNP_TMN_CODE, VNP_HASH_SECRET, VNP_URL)
