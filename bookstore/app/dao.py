import hashlib
from app import db, app, utils, mail
import uuid
from models import Customer, Staff, Book, Author, Category, User, UserRole, book_order, Order
from sqlalchemy import insert, func, cast, Float
from flask_mail import Message
from datetime import datetime


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


def add_order(orderID, customerID, phone, isPay, cart):
    if cart != None:
        order = Order(id=orderID, phone=phone, customer_id=customerID, isPay=isPay)
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


def update_order_status(orderID):
    order = Order.query.filter_by(id=orderID).first()
    order.isPay = True if order.isPay == False else False
    db.session.commit()


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


def load_book_by_id(bookID):
    return Book.query.get(bookID)

    
def load_books(kw=None, page=1, cate=None):
    books = Book.query

    if kw:
        books = books.filter(Book.name.icontains(kw))
    if cate:
        books = books.filter(Book.category_id.__eq__(cate))

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    books = books.slice(start, start + page_size)
    
    return books.all()


def count_books():
    return Book.query.count()


def load_orders(kw=None, customerID=None):
    orders = Order.query

    if kw:
        orders = orders.filter(Order.id.icontains(kw))

    return orders.all()


def calculate_order_total(order_id):
    total = db.session.query(
        db.func.sum(book_order.quantity * book_order.price)
    ).filter(book_order.order_id == order_id).scalar()

    return total or 0.0


def load_detail_order(orderID):
    order = Order.query.get(orderID)
    order_books = db.session.execute(db.select(book_order).filter_by(order_id=order.id)).fetchall()
    detailOrder = []
    for order_book in order_books:
        book  = Book.query.filter(Book.id == order_book.book_id).first()
        detailOrder.append({
            "id": order_book.book_id,
            "name": book.name,
            "author": book.author,
            "image": book.image,
            "price": int(order_book.price),
            "quantity": int(order_book.quantity),
            "total_price": int(order_book.price * order_book.quantity)
        })
    return detailOrder


def send_email(orderID, customerName):
    order = Order.query.get(orderID)

    orderData = load_detail_order(orderID)
    total = utils.total_price(orderData)

    email_body = f"""
    Hóa đơn bán sách

    Mã đơn hàng: {orderID}
    Tên khách hàng: {customerName}
    Tổng tiền: {total}
    
    Chi tiết đơn hàng:
    """
    for book in orderData:
        email_body += f"- {book['name']} (Mã: {book['id']}): {book['quantity']} quyển, Tác giả: {book['author']}\n"

    if order.isPay == False:
        email_body += f"\nPhương thức thanh toán: tiền mặt\n\n Sau 48 tiếng từ thời điểm đặt sách, nếu khách hàng không đến tiệm nhận sách thì đơn hàng sẽ bị hủy bỏ.\n"
    
    email_body += "\nCảm ơn quý khách đã mua hàng!"

    # Gửi email
    try:
        msg = Message(
            subject="Hóa đơn bán sách",
            recipients=["hung2004py@gmail.com"],  # Email người nhận
            body=email_body
        )
        mail.send(msg)
        return "Email đã được gửi thành công!"
    except Exception as e:
        return f"Không thể gửi email: {str(e)}"

# def revenue_stats(kw=None):
#     return db.session.query(
#         Category.id,
#         Category.name,
#         func.sum(book_order.c.price * book_order.c.quantity).label("total_revenue")
#     ) \
#     .join(Category, Category.id == Book.category_id) \
#     .join(Book, Book.id == book_order.c.book_id)\
#     .group_by(Category.id).all()

def revenue_stats(month=12, year=datetime.now().year):
    return db.session.query(
        Category.id,
        Category.name,
        func.sum(book_order.c.price * book_order.c.quantity).label("total_revenue"),
        func.sum(book_order.c.quantity).label("total_sales"),
        (func.sum(book_order.c.quantity) / cast(func.sum(func.sum(book_order.c.quantity)).over(), Float) * 100)
    )\
    .join(Book, Book.category_id == Category.id)\
    .join(book_order, book_order.c.book_id == Book.id)\
    .join(Order, book_order.c.order_id == Order.id)\
    .filter(func.extract('month', Order.createdDate) == month, func.extract('year', Order.createdDate) == year)\
    .group_by(Category.id).all()

def book_frequency_stats(month=12, year=datetime.now().year):
    total_quantity_subquery = db.session.query(
        func.sum(book_order.c.quantity).label("total_quantity")
    ).join(Order, book_order.c.order_id == Order.id)\
     .filter(
         func.extract('month', Order.createdDate) == month,
         func.extract('year', Order.createdDate) == year
     ).scalar_subquery()

    return db.session.query(
        Book.id.label("book_id"),
        Book.name.label("book_name"),
        Category.name.label("category_name"),
        func.sum(book_order.c.quantity).label("quantity"),
        (func.sum(book_order.c.quantity) / total_quantity_subquery * 100).label("percentage")
    )\
    .join(Category, Book.category_id == Category.id)\
    .join(book_order, book_order.c.book_id == Book.id)\
    .join(Order, book_order.c.order_id == Order.id)\
    .filter(
        func.extract('month', Order.createdDate) == month,
        func.extract('year', Order.createdDate) == year
    )\
    .group_by(Book.id, Category.name)\
    .all()

if __name__ == '__main__':
    with app.app_context():
        print(book_frequency_stats())
