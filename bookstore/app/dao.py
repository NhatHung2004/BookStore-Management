import hashlib
from app import db
from models import Customer, Staff, Book, Author, Category, User, UserRole


def add_user(phone, name, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, user_role=UserRole.CUSTOMER, avatar=avatar)
    customer = Customer(phone=phone, user=user)

    db.session.add(customer)
    db.session.commit()

    return customer


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User.query.filter(User.username.__eq__(username), User.password.__eq__(password))

    if role:
        user = user.filter(User.user_role.__eq__(role))

    return user.first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_cates():
    return Category.query.all()

    
def load_books(kw=None):
    books = Book.query

    if kw:
        books = books.filter(Book.name.icontains(kw))
    
    return books.all()


def load_books_by_cate(id):
    return Category.query.get(id).books
