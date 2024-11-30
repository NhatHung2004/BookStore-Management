from flask import Flask
from app.config import Config
import cloudinary
from app.extensions import db, migrate, login, admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    admin.init_app(app)

    cloudinary.config (
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],  # Click 'View API Keys' above to copy your API secret
        secure=True
    )
    # from app import models
    return app
