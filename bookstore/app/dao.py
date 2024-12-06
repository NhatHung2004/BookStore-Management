import hashlib
from app import db
from models import Customer, Staff, Book, Author, Category, User, UserRole, OnlineOrder, Bill, book_onlOrder
from sqlalchemy import insert


def add_user(phone, name, username, password, address, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, user_role=UserRole.CUSTOMER, avatar=avatar)
    customer = Customer(phone=phone, user=user, address=address)

    db.session.add(customer)
    db.session.commit()

    return customer


def add_to_book_onlOrder(book_id, onlOrder_id, quantity, price):
    # Tạo câu lệnh chèn vào bảng trung gian
    stmt = insert(book_onlOrder).values(
        book_id=book_id,
        onlOrder_id=onlOrder_id,
        quantity=quantity,
        price=price
    )
    # Thực thi câu lệnh
    db.session.execute(stmt)
    db.session.commit()


def add_online_order(customerID, cart):
    if cart != None:
        bill = Bill(customer_id=customerID)
        db.session.add(bill)
        db.session.flush()
        onlineOrder = OnlineOrder(customer_id=customerID, order=bill)
        db.session.add(onlineOrder)
        db.session.flush()
        for c in cart.values():
            add_to_book_onlOrder(
                book_id=int(c['id']),
                onlOrder_id=onlineOrder.id, 
                quantity=c['quantity'], 
                price=c['price']
            )
            
        db.session.commit()
        return onlineOrder.id
    return None


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
