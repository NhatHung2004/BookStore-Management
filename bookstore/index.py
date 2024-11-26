import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dao
from models import Customer
from flask import render_template, redirect, request
from flask_login import login_user, logout_user
from bookstore import app, login


@app.route("/")
def index():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login_process():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        if(role == "Customer"):
            user = dao.auth_user_customer(username=username, password=password)
        else:
            user = dao.auth_user_staff(username=username, password=password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Invalid username or password"
    return render_template("login.html", err_msg=err_msg)


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
        if not Customer.query.filter(Customer.username.__eq__(username)).first():
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
    role = request.form.get("role")
    return dao.get_user_by_id(user_id, role)


if __name__ == '__main__':
    from admin import *
    app.run(debug=True)