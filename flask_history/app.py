#coding=utf-8

import logging
from flask import Flask
from pymongo import MongoClient
from flask import make_response
from bson.json_util import dumps

app = Flask(__name__)


@app.route("/")
def all_history():
    logging.debug("Hello, Terminal")

    client = MongoClient('mongodb://mongo:27017/')
    coll = client.flask_desk_database['history_collection']
    ret = coll.find()

    resp = make_response(dumps(ret), 200)
    return resp
