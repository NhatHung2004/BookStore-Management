import hashlib
from app import db
from models import Customer, Staff, Book, Author, Type, User, UserRole


def add_user(phone, name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, user_role=UserRole.CUSTOMER)
    customer = Customer(phone=phone, user=user)

    db.session.add(customer)
    db.session.commit()

    return customer


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()
    return user


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_types():
    return Type.query.all()

    
def load_books(kw=None, type=None):
    books = db.session.query(Book, Author, Type).join(Author, Book.author_id == Author.id).join(Type, Book.type_id == Type.id)

    if kw:
        books = books.filter(Book.name.icontains(kw))
    if type:
        books = books.filter(Type.type.in_(type))

    return books.all()