from flask import Flask
from myapp import app

@app.route("/")
@app.route("/index")
def index_func():
    return "hello world!"