from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from vnpay import VNPay
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = 'HGHJAHA^&^&*AJAVAHJ*^&^&*%&*^GAFGFAG'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:1@localhost/storedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8
app.config["PAGE_MANAGE"] = 4
# Cấu hình email server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'goihot85@gmail.com'
app.config['MAIL_PASSWORD'] = 'ifevhqsigpuxoawa'
app.config['MAIL_DEFAULT_SENDER'] = 'goihot85@gmail.com'


db = SQLAlchemy(app)
login = LoginManager(app)
mail = Mail(app)


cloudinary.config(
    cloud_name="dvahhupo0",
    api_key="461556863519315",
    api_secret="lBLWun6CURjcaUNB8G7qUQtHtxo",  # Click 'View API Keys' above to copy your API secret
    secure=True
)


VNP_TMN_CODE = "265WA8JT"
VNP_HASH_SECRET = "R98T5GT4US65NUVY1IIINX8LWN9BM2G2"
VNP_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"

vnpay = VNPay(VNP_TMN_CODE, VNP_HASH_SECRET, VNP_URL)
