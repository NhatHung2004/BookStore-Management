import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cloudinary.uploader
from models import User, UserRole
from flask import render_template, redirect, request, session, jsonify
from flask_login import login_user, logout_user
from app import login, dao, app, utils
import cloudinary


@app.route("/")
def index():
    kw = request.args.get("kw")
    books = dao.load_books(kw=kw)
    return render_template("index.html", books=books)


@app.route('/category/<int:cate_id>')
def books_by_type(cate_id):
    books = dao.load_books_by_cate(cate_id)
    return render_template("index.html", books=books)


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
    session.modified = True

    return jsonify(utils.stats_cart(cart))


# @app.route('/api/updateQuantity/carts', methods=['post'])
# def update_quantity():
#     cart = session.get('cart')

#     id = str(request.json.get('id'))
#     cart[id]['quantity'] += 1

#     session['cart'] = cart

#     return jsonify({ "cart": cart[id] })


@app.route("/order-online")
def orderOnline():
    books = dao.load_books()
    return render_template("order_online.html", books=books)


@app.route("/unplaced-order")
def unplacedOrder():
    # books = dao.load_books()
    # return render_template("unplaced_order.html", books=books)
    return render_template("unplaced_order.html")


@app.route('/login', methods=['GET', 'POST'])
def login_process():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)
            return redirect('/')
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


@app.route("/logout", methods=['GET', 'POST'])
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register_process():
    err_msg = ""
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not User.query.filter(User.username.__eq__(username)).first():
            if password.strip() != confirm.strip():
                err_msg = "Mat khau khong khop"
            else:
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar = res["secure_url"]
                if dao.add_user(phone=phone, name=name, username=username, password=password, avatar=avatar):
                    return redirect('/login')
                else:
                    err_msg = "Something Wrong!!!"
        else:
            err_msg = "Username already exists"
    return render_template('register.html', err_msg=err_msg)


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
        "cart": session.get('cart')
    }


@app.template_filter('currency')
def currency_filter(value):
    return f"{value:,.0f} VND"


if __name__ == "__main__":
    from app import admin
    app.run(debug=True)
