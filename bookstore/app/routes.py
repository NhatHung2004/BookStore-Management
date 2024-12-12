import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import math
import cloudinary.uploader
from models import User, UserRole
from flask import render_template, redirect, request, session, jsonify, url_for
from flask_login import login_user, logout_user
from app import login, dao, app, utils, vnpay, VNP_HASH_SECRET
import hmac
import hashlib
import cloudinary
import urllib.parse


@app.route("/")
def index():
    kw = request.args.get("kw")
    cate = request.args.get("category")
    page = request.args.get('page', 1)
    total = dao.count_books()
    books = dao.load_books(kw=kw, page=int(page), cate=cate)
    message = session.pop('message', None)  # Lấy và xóa sau khi sử dụng
    order_id = session.pop('order_id', None)
    if message == "success":
        alert = f"Thanh toán thành công! Mã giao dịch: {order_id}"
        alert_type = "success"
    elif message == "failure":
        alert = "Xác thực giao dịch thất bại!"
        alert_type = "danger"
    else:
        alert = None
        alert_type = None
    return render_template("index.html", books=books, alert=alert, alert_type=alert_type,
                           pages=math.ceil(total / app.config["PAGE_SIZE"]))


@app.route("/cart")
def cart():
    books = dao.load_books()
    return render_template("cart.html", books=books)


@app.route('/api/add/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')

    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    author = request.json.get('author')
    category = request.json.get('category')
    image = request.json.get('image')
    price = request.json.get('price')

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "author": author,
            "category": category,
            "image": image,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/remove/carts', methods=['post'])
def remove_from_cart():
    cart = session.get('cart')

    id = str(request.json.get('id'))
    del cart[id]

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/updateQuantity/carts', methods=['post'])
def update_quantity():
    cart = session.get('cart')

    id = str(request.json.get('id'))
    cart[id]['quantity'] += 1

    session['cart'] = cart

    stats = utils.stats_cart(cart)

    return jsonify({ "total_quantity": stats['total_quantity'], 'quantity': cart[id]['quantity'], 'id': cart[id]['id'] })


@app.route("/list-order")
def orderOnline():
    kw = request.args.get("kw")
    orders = dao.load_orders(kw=kw)
    books = dao.load_books()
    return render_template("order_online.html", books=books, orders=orders)


@app.route("/order/")
def unplacedOrder():
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    total = dao.count_books()
    books = dao.load_books(kw=kw, page=int(page))
    return render_template("unplaced_order.html", books=books, pages=math.ceil(total / app.config["PAGE_SIZE"]))


@app.route("/order/<string:order_id>")
def order_details(order_id):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login_process():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)
            if user.user_role == UserRole.CUSTOMER:
                return redirect('/')
            else:
                return redirect('/order')
        else:
            err_msg = "Invalid username or password"
    return render_template("login.html", err_msg=err_msg)


@app.route("/login-admin", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
    if u:
        login_user(u)

    return redirect('/admin')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register_process():
    err_msg = ""
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        address = request.form.get("address")
        if not User.query.filter(User.username.__eq__(username)).first():
            if password.strip() != confirm.strip():
                err_msg = "Mat khau khong khop"
            else:
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar = res["secure_url"]
                if dao.add_user(phone=phone, name=name, username=username, password=password, address=address, avatar=avatar):
                    return redirect('/login')
                else:
                    err_msg = "Something Wrong!!!"
        else:
            err_msg = "Username already exists"
    return render_template('register.html', err_msg=err_msg)


@app.route("/api/checkout", methods=['POST'])
def checkout_api():
    customerID = request.json.get('customerID')
    cart = request.json.get('cart')
    phone = request.json.get('phone')

    orderID = dao.add_order(customerID=customerID, phone=phone, cart=cart)

    if orderID != None:
        session['cart'] = {}

    return jsonify({ "orderID": orderID, "stats": utils.stats_cart(cart)})


@app.route('/create_payment', methods=['POST'])
def create_payment():
    """Tạo URL thanh toán."""
    order_id = request.json.get('order_id')
    amount = int(request.json.get('amount'))
    ip_address = request.remote_addr

    payment_url = vnpay.create_payment_url(order_id, amount, 'http://127.0.0.1:5000/payment_success', ip_address)
    return jsonify({"payment_url": payment_url})


@app.route('/payment_success', methods=['GET'])
def payment_success():
    """Xử lý sau khi thanh toán."""
    vnp_params = request.args.to_dict()
    vnp_secure_hash = vnp_params.pop("vnp_SecureHash", None)

    # Sắp xếp tham số
    sorted_params = sorted(vnp_params.items())
    query_string = "&".join(f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in sorted_params)

    # Tạo hash
    generated_hash = hmac.new(
        VNP_HASH_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    if generated_hash.upper() == vnp_secure_hash.upper():  # So sánh không phân biệt hoa thường
        session['message'] = 'success'
        session['order_id'] = vnp_params.get('vnp_TxnRef')
        dao.update_order_status(vnp_params.get('vnp_TxnRef'))
        return redirect(url_for('index'))
    else:
        session['message'] = 'failure'
        return redirect(url_for('index'))
    

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_response():
    return {
        "cates" : dao.load_cates(),
        'cart_stats': utils.stats_cart(session.get('cart')),
        "cart": session.get('cart'),
        "UserRole": UserRole
    }


@app.template_filter('currency')
def currency_filter(value):
    return f"{value:,.0f} VND"


@app.route("/manage")
def manage():
    return render_template("manage.html")

@app.route("/detail-order")
def detail_order():
    return render_template("detail-order.html")

@app.route("/bill")
def bill():
    return render_template("bill.html")


if __name__ == "__main__":
    from app import admin
    app.run(debug=True)
