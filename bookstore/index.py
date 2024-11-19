import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import render_template, Flask
from bookstore import app


@app.route("/")
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)