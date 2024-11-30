import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Boolean
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from app import db, create_app
from datetime import date
import hashlib

app = create_app()

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

    books = relationship('Book', backref='author')

    def __str__(self):
        return self.name


class Type(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)

    books = relationship('Book', backref='type')

    def __str__(self):
        return self.type


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
    # author = relationship("Author", backref="books")
    # quan hệ one-to-many với bảng Type
    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    # type = relationship("Type", backref="books")


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
            }
        ]

        dataType = [
            {
                "type": "Nhân văn và sự kiện"
            },
            {
                "type": "Quản Trị - Lãnh Đạo"
            },
            {
                "type": "Tiểu thuyết"
            },
            {
                "type": "Lịch sử"
            },
        ]

        dataBook = [
            {
                "name": "Di Sản Hồ Chí Minh - Hành Trình Theo Chân Bác (Tái Bản 2021)",
                "inventoryQuantity": 100,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681292/image_237825_injgum.webp",
                "price": 99,
                "author_id": 1,
                "type_id": 1
            },
            {
                "name": "Quản Trị Bằng Văn Hóa - Cách Thức Kiến Tạo Và Tái Tạo Văn Hóa Tổ Chức",
                "inventoryQuantity": 78,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681282/8935280401068_wnlrtk.webp",
                "price": 99,
                "author_id": 2,
                "type_id": 2
            },
            {
                "name": "Không Gia Đình",
                "inventoryQuantity": 50,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681286/image_190973_ghrqko.webp",
                "price": 99,
                "author_id": 3,
                "type_id": 3
            },
            {
                "name": "Cây Cam Ngọt Của Tôi",
                "inventoryQuantity": 50,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732681983/image_217480_xmdzew.webp",
                "price": 99,
                "author_id": 4,
                "type_id": 3
            },
            {
                "name": "Di Chúc Của Chủ Tịch Hồ Chí Minh",
                "inventoryQuantity": 124,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732682133/9786045892640_pjzzzm.webp",
                "price": 99,
                "author_id": 5,
                "type_id": 1
            },
            {
                "name": "Đi Dọc Dòng Sông Phật Giáo",
                "inventoryQuantity": 5,
                "image": "https://res.cloudinary.com/dvahhupo0/image/upload/v1732682344/5819c3669f12f4487bd77ea4a0107d4b.jpg_rxmwwn.webp",
                "price": 99,
                "author_id": 1,
                "type_id": 1
            },
        ]

        # for p in dataType:
        #     prod = Type(type=p['type'])
        #     db.session.add(prod)
        # db.session.commit()

        # for p in dataAuthor:
        #     prod = Author(name=p['name'])
        #     db.session.add(prod)
        # db.session.commit()

        # for p in dataBook:
        #     prod = Book(name=p['name'], inventoryQuantity=p['inventoryQuantity'], image=p['image'], price=p['price'], author_id=p['author_id'], type_id=p['type_id'],)
        #     db.session.add(prod)
        # db.session.commit()