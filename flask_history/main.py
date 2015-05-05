#!/bin/env python

import logging
import click
import json
from bson import json_util
from pprint import pformat


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
    logging.info("starting redis subs")
    import redis
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


if __name__ == "__main__":
    cli()
