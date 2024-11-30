import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import User, UserRole
from flask import render_template, redirect, request
from flask_login import login_user, logout_user
from app import login, dao, create_app

app = create_app()


@app.route("/")
def index():
    kw = request.args.get('kw')
    type = request.args.getlist("type")
    books = dao.load_books(kw=kw, type=type)
    types = dao.load_types()
    return render_template("index.html", books=books, types=types)

@app.route("/cart")
def cart():
    books = dao.load_books()
    return render_template("cart.html", books=books)

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
                if dao.add_user(phone=phone, name=name, username=username, password=password):
                    return redirect('/login')
                else:
                    err_msg = "Something Wrong!!!"
        else:
            err_msg = "Username already exists"
    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    from admin import *
    app.run(debug=True)
