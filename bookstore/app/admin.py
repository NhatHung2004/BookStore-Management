from flask_admin.contrib.sqla import ModelView
from app import db, admin
from models import Staff, Book, Type, Author


admin.add_view(ModelView(Book, db.session))

admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Author, db.session))
