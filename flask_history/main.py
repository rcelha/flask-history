#!/bin/env python

import logging
import click
import json
from bson import json_util
from pprint import pformat

from pymongo import MongoClient
import redis
import dictdiffer


logging.getLogger().setLevel(logging.DEBUG)


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    logging.info("Flask desk runner")
    from app import app
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)


@cli.command()
def consume():
    client = MongoClient('mongodb://mongo:27017/')
    coll = client.flask_desk_database['history_collection']

    logging.info("starting redis subs")
    r = redis.StrictRedis(host='flaskdesk_redis', port=6379, db=0)
    ps = r.pubsub()
    ps.subscribe('ticket-data')
    for message in ps.listen():
        logging.info("Message received")
        logging.info(message)
        try:
            data = message['data']
            if isinstance(data, bytes):
                data = data.decode()
            data = json_util.loads(data)
        except Exception as e:
            logging.error("couldn't parse the message '%s'" % data)
            logging.error(e)
            continue
        logging.info("Old")
        logging.info(pformat(data['old_ticket']))
        logging.info("New")
        logging.info(pformat(data['new_ticket']))

        if not data['old_ticket']:
            data['old_ticket'] = {}

        diff = dictdiffer.diff(data['old_ticket'],
                               data['new_ticket'])
        diff = list(diff)
        if not diff:
            continue

        rec = coll.update_one(
            filter={
                "ticket_id": data['new_ticket']['_id']
            },
            update={
                '$inc': {'rev': 1},
                '$push': {
                    'log': diff
                }
            },
            upsert=True)
        logging.info("recorderd object")
        logging.info(rec)

if __name__ == "__main__":
    cli()
