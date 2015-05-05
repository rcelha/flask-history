#coding=utf-8

import logging
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    logging.debug("Hello, Terminal")
    return "Hello, Moto"
