import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Boolean
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from app import db, app
from datetime import date
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
    user_role = Column(Enum(UserRole), nullable=False)
    avatar = Column(String(250), default='https://res.cloudinary.com/dvahhupo0/image/upload/v1733131895/user_e5uokm.jpg')

    customer = relationship('Customer', backref='user', uselist=False)
    staff = relationship('Staff', backref='user', uselist=False)

    

class Customer(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    phone = Column(String(50))
    address = Column(String(100))

    onlineOrders = relationship('OnlineOrder', backref='customer', lazy=True)
    bills = relationship('Bill', backref='customer', lazy=True)
    

class Staff(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    phone = Column(String(50))
    role_permision = Column(Enum(RolePermision), nullable=False)

    # quan hệ one-to-many với bảng OnlineOrder
    onlineOrders = relationship('OnlineOrder', backref='staff', lazy=True)
    # quan hệ one-to-many với bảng Bill
    bills = relationship('Bill', backref='staff', lazy=True)
    # quan hệ one-to-many với bảng BookEntryForm
    bookEntryForms = relationship('BookEntryForm', backref='staff', lazy=True)


class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdDate = Column(Date, default=date.today())

    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)

    onlineOrder = relationship("OnlineOrder", backref="order", lazy=True, uselist=False)

    books = relationship('BillDetail', backref='bill')


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

    # quan hệ many-to-many với bảng OnlineOrder
    onlineOrders = relationship('OnlineOrderDetail', backref='book')
    # quan hệ many-to-many với bảng Bill
    bills = relationship('BillDetail', backref='book')
    # quan hệ many-to-many với bảng BookEntryForm
    bookEntryForms = relationship('BookEntryFormDetail', backref='book')
    # quan hệ one-to-many với bảng Author
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    # quan hệ one-to-many với bảng Category
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


class OnlineOrder(db.Model):
    onlineOrder_id = Column(Integer, ForeignKey(Bill.id), primary_key=True)
    createdDate = Column(Date, default=date.today(), nullable=False)
    pickupDate = Column(Date, default=date.today(), nullable=False)
    isPay = Column(Boolean, default=False)

    # quan hệ one-to-many với bảng Customer và bảng Staff
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    
    # quan hệ many-to-many với bảng Book
    books = relationship('OnlineOrderDetail', backref='onlineOrder')


class BookEntryForm(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdDate = Column(Date, default=date.today())
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)

    books = relationship('BookEntryFormDetail', backref='bookEntryForm')


class OnlineOrderDetail(db.Model):
    book_id = Column(ForeignKey(Book.id), primary_key=True)
    onlineOrder_id = Column(ForeignKey(OnlineOrder.onlineOrder_id), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class BillDetail(db.Model):
    bill_id = Column(ForeignKey(Bill.id), primary_key=True)
    book_id = Column(ForeignKey(Book.id), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class BookEntryFormDetail(db.Model):
    bookEntryForm_id = Column(ForeignKey(BookEntryForm.id), primary_key=True)
    book_id = Column(ForeignKey(Book.id), primary_key=True)
    quantity = Column(Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # admin = User(name="Admin", username="admin", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRole.ADMIN)
        # db.session.add(admin)
        # db.session.commit()
        # manager = User(name='Manager', username='manager',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRole.STAFF)
        # m = Staff(phone='123456789', role_permision=RolePermision.MANAGER, user=manager)

        # seller = User(name='Seller', username='seller',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRole.STAFF)
        # s = Staff(phone='123456789', role_permision=RolePermision.SELLER, user=seller)
        # db.session.add_all([m, s])
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
            },
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