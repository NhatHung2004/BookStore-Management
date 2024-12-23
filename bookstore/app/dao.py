import hashlib
from app import db, app, utils, mail
import uuid
from models import Customer, Staff, Book, Author, Category, User, UserRole, OrderDetails, Order, Comment, FormDetails, Form, ImportRule
from flask_mail import Message
from flask_login import current_user
from sqlalchemy import func, cast, Float
from datetime import datetime


def add_user(phone, name, username, password, address, email, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, user_role=UserRole.CUSTOMER, avatar=avatar, email=email)
    customer = Customer(phone=phone, user=user, address=address)

    db.session.add(customer)
    db.session.commit()

    return customer


def update_profile(name, phone, address, email):
    customer = Customer.query.filter(Customer.id == current_user.id).first()
    customer.phone = phone
    customer.address = address
    customer.user.name = name
    customer.user.email = email
    db.session.commit()


def add_order(orderID, customerID, phone, isPay, cart):
    if cart != None:
        if customerID == None:
            customer = Customer.query.filter(Customer.phone==phone).first()
            if customer != None:
                order = Order(id=orderID, phone=phone, customer_id=customer.id, isPay=isPay, staff_id=current_user.id)
            else:
                order = Order(id=orderID, phone=phone, isPay=isPay, staff_id=current_user.id)
        else:
            order = Order(id=orderID, phone=phone, customer_id=customerID, isPay=isPay)
        db.session.add(order)

        for c in cart.values():
            d = OrderDetails(book_id=int(c['id']), order=order, quantity=c['quantity'], unit_price=c['price'])
            db.session.add(d)
            
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
    books = books.order_by(Book.id.desc())

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


def delete_book(bookID):
    book = Book.query.get(bookID)
    if not book:
        return 0
    db.session.delete(book)
    db.session.commit()
    return 1


def update_book(bookID, inventoryQuantity):
    book = Book.query.filter(Book.id.__eq__(bookID)).first()
    r = ImportRule.query.first()

    if not book:
        return {"message": "Sách không tồn tại!", "status": "fail"}
    
    if book.inventoryQuantity >= r.max_quantity:
        return {"message": "Chỉ cập nhật sách có số lượng dưới 300!", "status": "fail"}

    if inventoryQuantity >= r.min_quantity:
        book.inventoryQuantity += inventoryQuantity
        db.session.commit()
        return {"message": "Cập nhật số lượng sách thành công!", "status": "success"}
    
    return {"message": "Số lượng sách không hợp lệ!", "status": "fail"}


def add_form(form):
    fo = Form(staff_id=current_user.id)
    db.session.add(fo)

    for f in form.values():
        d = FormDetails(book_id=f['bookID'], form=fo, quantity=f['inventoryQuantity'])
        db.session.add(d)
    
    db.session.commit()

    return fo.id


def load_forms(formID=None):
    if formID:
        return Form.query.filter(Form.id.__eq__(formID)).first()


def add_book(name, author, price, inventoryQuantity, category, image):
    au = Author.query.filter(Author.name.__eq__(author)).first()
    cate = Category.query.filter(Category.name.__eq__(category)).first()

    if not au:
        au = Author(name=author)
        db.session.add(au)

    book = Book(name=name, author=au, price=price, inventoryQuantity=inventoryQuantity, category=cate, image=image)
    db.session.add(book)
    db.session.commit()
    return book


def load_orders(kw=None):
    orders = Order.query

    if kw:
        orders = orders.filter(Order.id.icontains(kw))

    return orders.all()


def add_comment(content, book_id):
    c = Comment(content=content, book_id=book_id, customer=current_user.customer)
    db.session.add(c)
    db.session.commit()
    return c


def calculate_order_total(order_id):
    total = db.session.query(func.sum(OrderDetails.quantity * OrderDetails.unit_price)
    ).filter(OrderDetails.order_id == order_id).scalar()

    return total or 0.0


def load_detail_order(orderID):
    order_books = OrderDetails.query.filter(OrderDetails.order_id.__eq__(orderID)).all()
    detailOrder = []
    for order_book in order_books:
        book  = Book.query.filter(Book.id == order_book.book_id).first()
        detailOrder.append({
            "id": order_book.book_id,
            "name": book.name,
            "author": book.author,
            "image": book.image,
            "price": int(order_book.unit_price),
            "quantity": int(order_book.quantity),
            "total_price": int(order_book.unit_price * order_book.quantity)
        })
    return detailOrder


def load_bill(orderID):
    order = OrderDetails.query.filter(OrderDetails.order_id.__eq__(orderID)).all()
    bill = []
    for o in order:
        bill.append({
            "id": o.book_id,
            "name": o.book.name,
            "category": o.book.category.name,
            "price": o.unit_price,
            "quantity": o.quantity,
            "totalUnitPrice": int(o.unit_price * o.quantity)
        })
    return bill


def load_bill_info(orderID):
    order = Order.query.get(orderID)

    if order.customer_id != None:
        cusID = order.customer_id
        cusName = order.customer.user.name
    else:
        cusID = 0
        cusName = ""

    if order.staff_id != None:
        staffID = order.staff_id
        staffName = order.staff.user.name
    else:
        staffID = 0
        staffName = ""

    return {
        "cusID": cusID,
        "staffID": staffID,
        "cusName": cusName,
        "staffName": staffName,
        "createdDate": order.createdDate,
        "totalPrice": db.session.query(func.sum(OrderDetails.quantity * OrderDetails.unit_price))
                                .filter(OrderDetails.order_id.__eq__(orderID)).scalar()
    }


def send_email(orderID, customerName, address, email):
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
    
    email_body += "\nĐịa chỉ giao hàng: " + address
    email_body += "\nCảm ơn quý khách đã mua hàng!"

    # Gửi email
    try:
        msg = Message(
            subject="Hóa đơn bán sách",
            recipients=[email],  # Email người nhận
            body=email_body
        )
        mail.send(msg)
        return "Email đã được gửi thành công!"
    except Exception as e:
        return f"Không thể gửi email: {str(e)}"
    

def month_revenue_stats(month=12, year=datetime.now().year):
    return db.session.query(
        Category.id, Category.name,
        func.sum(OrderDetails.unit_price * OrderDetails.quantity).label("Tổng doanh thu"),
        func.sum(OrderDetails.quantity).label("Số lượng bán"),
        (func.sum(OrderDetails.quantity) / cast(func.sum(func.sum(OrderDetails.quantity)).over(), Float) * 100).label("Phần trăm lượt bán")
    ).join(Book, Book.category_id == Category.id).join(OrderDetails, OrderDetails.book_id == Book.id)\
    .join(Order, OrderDetails.order_id == Order.id).filter(func.extract('month', Order.createdDate) == month, func.extract('year', Order.createdDate) == year)\
    .group_by(Category.id).all()


def book_frequency_stats(month=12, year=datetime.now().year):
    with app.app_context():
        total_quantity_subquery = db.session.query(
            func.sum(OrderDetails.quantity).label("total_quantity")
        ).join(Order, OrderDetails.order_id == Order.id)\
         .filter(
             func.extract('month', Order.createdDate) == month,
             func.extract('year', Order.createdDate) == year
         ).scalar_subquery()

        return db.session.query(
            Book.id.label("book_id"),
            Book.name.label("book_name"),
            Category.name.label("category_name"),
            func.sum(OrderDetails.quantity).label("quantity_sold"),
            (func.sum(OrderDetails.quantity) / total_quantity_subquery * 100).label("percentage_of_total_quantity_sold")
        )\
        .join(Category, Book.category_id == Category.id)\
        .join(OrderDetails, OrderDetails.book_id == Book.id)\
        .join(Order, OrderDetails.order_id == Order.id)\
        .filter(
            func.extract('month', Order.createdDate) == month,
            func.extract('year', Order.createdDate) == year
        )\
        .group_by(Book.id, Category.name)\
        .all()
