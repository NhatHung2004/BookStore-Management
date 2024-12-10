from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from vnpay import VNPay


app = Flask(__name__)
app.secret_key = 'HGHJAHA^&^&*AJAVAHJ*^&^&*%&*^GAFGFAG'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://NhatHung:nhathung123@localhost/storedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8


db = SQLAlchemy(app)
login = LoginManager(app)


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
