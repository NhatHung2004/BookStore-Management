import os


class Config:
    SECRET_KEY = 'HGHJAHA^&^&*AJAVAHJ*^&^&*%&*^GAFGFAG'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://NhatHung:nhathung123@localhost/storedb?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_SIZE = 4
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'dvahhupo0')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '461556863519315')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'lBLWun6CURjcaUNB8G7qUQtHtxo')
    PAGE_SIZE = 4