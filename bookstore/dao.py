import hashlib
from bookstore import db
from models import Customer, Staff, Book, Author, Type


def add_user(phone, name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    customer = Customer(phone=phone, name=name, username=username, password=password)

    db.session.add(customer)
    db.session.commit()

    return customer


def auth_user_customer(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Customer.query.filter(Customer.username.__eq__(username), Customer.password.__eq__(password)).first()


def auth_user_staff(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Staff.query.filter(Staff.username.__eq__(username), Staff.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return Customer.query.get(user_id)


def load_types():
    return Type.query.all()

    
def load_books(kw=None, type=None):
    books = db.session.query(Book, Author, Type).join(Author, Book.author_id == Author.id).join(Type, Book.type_id == Type.id)

    if kw:
        books = books.filter(Book.name.icontains(kw))
    if type:
        books = books.filter(Type.type.in_(type))

    return books.all()