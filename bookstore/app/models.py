import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from enum import Enum as RoleEnum
from app import db, app
from datetime import datetime
import hashlib

# quyền của nhân viên
class RolePermision(RoleEnum):
    MANAGER = 1
    SELLER = 2


# vai trò người dùng
class UserRole(RoleEnum):
    ADMIN = 1
    STAFF = 2
    CUSTOMER = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)
    avatar = Column(String(250), default='https://res.cloudinary.com/dvahhupo0/image/upload/v1733131895/user_e5uokm.jpg')

    customer = relationship('Customer', backref='user', uselist=False)
    staff = relationship('Staff', backref='user', uselist=False)

    

class Customer(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    phone = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)

    orders = relationship('Order', backref='customer', lazy=True)
    comments = relationship('Comment', backref='customer', lazy=True)
    

class Staff(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    phone = Column(String(50))
    role_permision = Column(Enum(RolePermision), nullable=False)

    orders = relationship('Order', backref='staff', lazy=True)
    forms = relationship('Form', backref='staff', lazy=True)


class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    books = relationship('Book', backref='author', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False, unique=True)
    inventoryQuantity = Column(Integer, nullable=False)
    image = Column(String(300), nullable=True,
                    default="https://res.cloudinary.com/dvahhupo0/image/upload/v1732094791/samples/cloudinary-icon.png")
    price = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    order_details = relationship("OrderDetails", backref="book", lazy=True)
    form_details = relationship("FormDetails", backref="book", lazy=True)
    comments = relationship("Comment", backref="book", lazy=True)

    def __str__(self):
        return self.name


class Order(db.Model):
    id = Column(String(50), primary_key=True)
    createdDate = Column(DateTime, default=datetime.now(), nullable=False)
    isPay = Column(Boolean, default=False)
    phone = Column(String(20), nullable=True)

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=True)

    order_details = relationship("OrderDetails", backref="order", lazy=True)


class Form(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdDate = Column(DateTime, default=datetime.now())
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)

    form_details = relationship("FormDetails", backref="form", lazy=True)


class OrderDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    order_id = Column(String(50), ForeignKey(Order.id), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Integer, nullable=False, default=0)


class FormDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    form_id = Column(Integer, ForeignKey(Form.id), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)


class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # admin = User(name="Admin", username="admin", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             email="admin@gmail.com", user_role=UserRole.ADMIN)
        # db.session.add(admin)
        # db.session.commit()
        # manager = User(name='Manager', username='manager',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             email="manager@gmail.com", user_role=UserRole.STAFF)
        # m = Staff(phone='123456789', role_permision=RolePermision.MANAGER, user=manager)

        # seller = User(name='Seller', username='seller',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             email="seller@gmail.com", user_role=UserRole.STAFF)
        # s = Staff(phone='123456789', role_permision=RolePermision.SELLER, user=seller)
        # db.session.add_all([m, s])
        # db.session.commit()

        # customer = User(name="Nguyễn Nhật Hưng", username="nhathung",
        #                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                 email="hung2004py@gmail.com", user_role=UserRole.CUSTOMER,
        #                 avatar="https://res.cloudinary.com/dvahhupo0/image/upload/v1733470370/vbwqwhu5l0w8cf3yljux.jpg")
        # c = Customer(phone="0836367981", address="Nhà Bè", user=customer)
        # db.session.add(c)
        # db.session.commit()

        dataAuthor = [
            {
                "name": "Trần Đức Tuấn"
            },
            {
                "name": "Giản Tư Trung"
            },
            {
                "name": "Huỳnh Lý"
            },
            {
                "name": "José Mauro de Vasconcelos"
            },
            {
                "name": "Chủ tịch Hồ Chí Minh"
            },
            {
                "name": "Yuval Noah Harari"
            },
            {
                "name": "Nam Phong Tùng Thư"
            },
            {
                "name": "Jared Diamond"
            },
            {
                "name": "Phan Văn Trường"
            }
        ]

        dataCategory = [
            {
                "name": "Nhân văn và sự kiện"
            },
            {
                "name": "Quản Trị - Lãnh Đạo"
            },
            {
                "name": "Tiểu thuyết"
            },
            {
                "name": "Lịch sử"
            },
        ]

        dataBook = [
            {
                "name": "Di Sản Hồ Chí Minh - Hành Trình Theo Chân Bác (Tái Bản 2021)",
                "inventoryQuantity": 100,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681292/image_237825_injgum.webp",
                "price": 96000,
                "author_id": 1,
                "category_id": 1
            },
            {
                "name": "Quản Trị Bằng Văn Hóa - Cách Thức Kiến Tạo Và Tái Tạo Văn Hóa Tổ Chức",
                "inventoryQuantity": 78,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681282/8935280401068_wnlrtk.webp",
                "price": 175000,
                "author_id": 2,
                "category_id": 2
            },
            {
                "name": "Không Gia Đình",
                "inventoryQuantity": 115,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681286/image_190973_ghrqko.webp",
                "price": 99000,
                "author_id": 3,
                "category_id": 3
            },
            {
                "name": "Cây Cam Ngọt Của Tôi",
                "inventoryQuantity": 50,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681983/image_217480_xmdzew.webp",
                "price": 81000,
                "author_id": 4,
                "category_id": 3
            },
            {
                "name": "Di Chúc Của Chủ Tịch Hồ Chí Minh",
                "inventoryQuantity": 124,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732682133/9786045892640_pjzzzm.webp",
                "price": 20000,
                "author_id": 5,
                "category_id": 1
            },
            {
                "name": "Đi Dọc Dòng Sông Phật Giáo",
                "inventoryQuantity": 5,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732682344/5819c3669f12f4487bd77ea4a0107d4b.jpg_rxmwwn.webp",
                "price": 70000,
                "author_id": 1,
                "category_id": 1
            },
            {
                "name": "Sapiens Lược Sử Loài Người",
                "inventoryQuantity": 10,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733281851/8935270703554_xkwlgz.webp",
                "price": 230000,
                "author_id": 6,
                "category_id": 4
            },
            {
                "name": "Lịch Sử Thế Giới",
                "inventoryQuantity": 54,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733282144/image_195509_1_39442_tqqj9h.webp",
                "price": 61000,
                "author_id": 7,
                "category_id": 4
            },
            {
                "name": "Súng, Vi Trùng Và Thép (Tái Bản)",
                "inventoryQuantity": 194,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733282253/8935270703837_hqyrwi.webp",
                "price": 261000,
                "author_id": 8,
                "category_id": 4
            },
            {
                "name": "Lịch Sử Và Học Thuyết Của Voltaire",
                "inventoryQuantity": 32,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733282407/47428666a6baa0505014e07398493afb.jpg_ejkjvc.webp",
                "price": 71000,
                "author_id": 7,
                "category_id": 4
            },
            {
                "name": "Vun Đắp Tâm Hồn - Tiệm Bánh Của Thỏ Mina",
                "inventoryQuantity": 18,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733282609/515d86965a6f9b4d639726cebaca6619.jpg_hseyv8.webp",
                "price": 45000,
                "author_id": 3,
                "category_id": 3
            },
            {
                "name": "Chuyện Kể Trước Giờ Đi Ngủ: Giấc Mơ Bơ Cà Rốt",
                "inventoryQuantity": 100,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733282684/961f1400e47b123cb0dd8d681312a8a8.jpg_zkweli.webp",
                "price": 56000,
                "author_id": 3,
                "category_id": 3
            },
            {
                "name": "Một Đời Quản Trị (Tái Bản 2019)",
                "inventoryQuantity": 610,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733282895/8934974164623_ogy5ya.webp",
                "price": 154000,
                "author_id": 9,
                "category_id": 2
            },
            {
                "name": "Cơn lốc quản trị - Ba trụ cột của văn hóa doanh nghiệp",
                "inventoryQuantity": 200,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1733283038/58c17950e24e1f9b0b08221edec27dc5.jpg_bueomz.webp",
                "price": 93000,
                "author_id": 9,
                "category_id": 2
            }
        ]

        # for p in dataCategory:
        #     prod = Category(name=p['name'])
        #     db.session.add(prod)
        # db.session.commit()

        # for p in dataAuthor:
        #     prod = Author(name=p['name'])
        #     db.session.add(prod)
        # db.session.commit()

        # for p in dataBook:
        #     prod = Book(name=p['name'], inventoryQuantity=p['inventoryQuantity'], image=p['image'], price=p['price'], author_id=p['author_id'], category_id=p['category_id'],)
        #     db.session.add(prod)
        # db.session.commit()