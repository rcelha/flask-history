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
    logging.info("Flask history consumer")
    import consumer
    consumer.consume()

if __name__ == "__main__":
    cli()
