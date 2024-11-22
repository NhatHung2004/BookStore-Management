import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import render_template
from bookstore import app


@app.route("/")
def index():
    return "Hello World"

@app.route('/login')
def login_process():
    return render_template('login.html')

@app.route('/register')
def register_process():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)