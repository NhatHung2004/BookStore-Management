import hashlib
from app import db, app
from models import Customer, Staff, Book, Author, Category, User, UserRole, book_order, Order
from sqlalchemy import insert


def add_user(phone, name, username, password, address, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, user_role=UserRole.CUSTOMER, avatar=avatar)
    customer = Customer(phone=phone, user=user, address=address)

    db.session.add(customer)
    db.session.commit()

    return customer


def add_to_book_order(book_id, order_id, quantity, price):
    # Tạo câu lệnh chèn vào bảng trung gian
    stmt = insert(book_order).values(
        book_id=book_id,
        order_id=order_id,
        quantity=quantity,
        price=price
    )
    # Thực thi câu lệnh
    db.session.execute(stmt)
    db.session.commit()


def add_order(customerID, phone, cart):
    if cart != None:
        order = Order(phone=phone, customer_id=customerID)
        db.session.add(order)
        db.session.flush()

        for c in cart.values():
            add_to_book_order(
                book_id=int(c['id']),
                order_id=order.id, 
                quantity=c['quantity'], 
                price=c['price']
            )
            
        db.session.commit()
        return order.id
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

    
def load_books(kw=None, page=1):
    books = Book.query

    if kw:
        books = books.filter(Book.name.icontains(kw))

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    books = books.slice(start, start + page_size)
    
    return books.all()


def count_books():
    return Book.query.count()


def load_books_by_cate(id):
    return Category.query.get(id).books
