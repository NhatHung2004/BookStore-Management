from flask_admin.contrib.sqla import ModelView
from models import Staff, Book, Type, Author
from bookstore import db, admin
from wtforms import SelectField


admin.add_view(ModelView(Book, db.session))

admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Author, db.session))
