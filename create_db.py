#! /usr/bin/env python

import MySQLdb
import json
import argparse
import getpass
from db import get_connection_config, get_engine, Base, DB_NAME
from product.models.identity import	CardIdentity
from product.models.pricing import CardPricingType, CardPricing, CardPriceSnapshot


def get_connection(username=None, password=None, host=None):
	return MySQLdb.connect(
		user=username,
		password=password,
		host=host
	)


def get_connection_from_config():
	config = get_connection_config()
	return get_connection(**config)

class Password(argparse.Action):
	def __call__(self, parser, namespace, values, option_string):
		if values is None:
			values = getpass.getpass()
		setattr(namespace, self.dest, values)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--username', required=False)
	parser.add_argument('-p', '--password', required=False, action=Password)
	parser.add_argument('--host', required=False)
	parser.add_argument('-f', '--force-drop', required=False, help='Drop existing DB and re-create empty', action='store_true')
	args = parser.parse_args()
	username, password = args.username, args.password
	host = args.host
	if not (username and password and host):
		config = get_connection_config()
		if not username and not password:
			username, password = config.get('username'), config.get('password')
		if not host:
			host = config.get('host')

	connection = get_connection(
		username=username,
		password=password,
		host=host
	)

	cursor = connection.cursor()
	cursor.execute('SHOW DATABASES;')
	dbs = [dbname[0] for dbname in cursor.fetchall()]
	if DB_NAME in dbs:
		if not args.force_drop:
			raise Exception(f'db "{DB_NAME}" already exists and there is no --force-drop flag; aborting')
		cursor.execute(f'DROP DATABASE {DB_NAME};')
	cursor.execute(f'CREATE DATABASE {DB_NAME};')
	cursor = connection.cursor()

	engine = get_engine()
	Base.metadata.create_all(engine)
