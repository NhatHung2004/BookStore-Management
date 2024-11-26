import hashlib
from bookstore import db
from models import Customer, Staff


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


def get_user_by_id(user_id, role):
    if role == "Customer":
        return Customer.query.get(user_id)
    else:
        return Staff.query.get(user_id)