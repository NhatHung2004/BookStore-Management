import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from bookstore import app, db
from datetime import date

# quyền của nhân viên
class RolePermision(RoleEnum):
    MANAGER = 1
    SELLER = 2


# vai trò người dùng
class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class Account(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    customer = relationship("Customer", backref="account", lazy=True, uselist=False)
    staff = relationship("Staff", backref="account", lazy=True, uselist=False)
    

class Customer(db.Model):
    account_id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    ten = Column(String(50), nullable=False)
    soDienThoai = Column(String(50))
    address = Column(String(100))

    onlineOrders = relationship('OnlineOrder', backref='customer', lazy=True)
    bills = relationship('Bill', backref='customer', lazy=True)
    

class Staff(db.Model):
    account_id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    ten = Column(String(50), nullable=False)
    soDienThoai = Column(String(50))
    role_permision = Column(Enum(RolePermision))

    # quan hệ one-to-many với bảng OnlineOrder
    onlineOrders = relationship('OnlineOrder', backref='staff', lazy=True)
    # quan hệ one-to-many với bảng Bill
    bills = relationship('Bill', backref='staff', lazy=True)
    # quan hệ one-to-many với bảng PurchaseOrder
    purchaseOrders = relationship('PurchaseOrder', backref='staff', lazy=True)


class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayXuat = Column(Date, default=date.today())

    customer_id = Column(Integer, ForeignKey(Customer.account_id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.account_id), nullable=False)

    onlineOrder = relationship("OnlineOrder", backref="order", lazy=True, uselist=False)

    books = relationship('BillDetail', backref='bill')


class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)

    books = relationship('Book', backref='author', lazy=True)


class Type(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)

    books = relationship('Book', backref='type', lazy=True)


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False, unique=True)
    soLuongTon = Column(Integer, nullable=False)

    # quan hệ many-to-many với bảng OnlineOrder
    onlineOrders = relationship('OnlineOrderDetail', backref='book')
    # quan hệ many-to-many với bảng Bill
    bills = relationship('BillDetail', backref='book')
    # quan hệ many-to-many với bảng PurchaseOrder
    purchaseOrders = relationship('PurchaseOrderDetail', backref='book')
    # quan hệ one-to-many với bảng Author
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    # quan hệ one-to-many với bảng Type
    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)


class OnlineOrder(db.Model):
    onlineOrder_id = Column(Integer, ForeignKey(Bill.id), primary_key=True)
    ngayTao = Column(Date, default=date.today(), nullable=False)
    ngayLayHang = Column(Date, default=date.today(), nullable=False)
    thanhToan = Column(Boolean, default=False)

    # quan hệ one-to-many với bảng Customer và bảng Staff
    customer_id = Column(Integer, ForeignKey(Customer.account_id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.account_id), nullable=False)
    
    # quan hệ many-to-many với bảng Book
    books = relationship('OnlineOrderDetail', backref='onlineOrder')


class PurchaseOrder(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayNhap = Column(Date, default=date.today())
    staff_id = Column(Integer, ForeignKey(Staff.account_id), nullable=False)

    books = relationship('PurchaseOrderDetail', backref='purchaseOrder')


class OnlineOrderDetail(db.Model):
    book_id = Column(ForeignKey(Book.id), primary_key=True)
    onlineOrder_id = Column(ForeignKey(OnlineOrder.onlineOrder_id), primary_key=True)
    soLuong = Column(Integer, nullable=False)
    gia = Column(Integer, nullable=False)


class BillDetail(db.Model):
    bill_id = Column(ForeignKey(Bill.id), primary_key=True)
    book_id = Column(ForeignKey(Book.id), primary_key=True)
    soLuong = Column(Integer, nullable=False)
    gia = Column(Integer, nullable=False)


class PurchaseOrderDetail(db.Model):
    purchaseOrder_id = Column(ForeignKey(PurchaseOrder.id), primary_key=True)
    book_id = Column(ForeignKey(Book.id), primary_key=True)
    soLuong = Column(Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # u1 = Account(username="admin", password="123", user_role=UserRole.ADMIN)
        # u2 = Account(username="seller", password="123", user_role=UserRole.USER)
        # u3 = Account(username="customer", password="123", user_role=UserRole.USER)
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()

        # c = Customer(id=3, ten="Customer", soDienThoai="123456789")
        # db.session.add(c)
        # db.session.commit()