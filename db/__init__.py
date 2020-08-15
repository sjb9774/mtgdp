from sqlalchemy import create_engine
import MySQLdb
import json
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_connection_config():
	with open('credentials/db.json', 'r') as f:
		config = json.loads(f.read())
	return config


def get_connection(username=None, password=None, host=None):
	return MySQLdb.connect(
		user=username,
		password=password,
		host=host
	)


def get_connection_from_config():
	config = get_connection_config()
	return get_connection(**config)


def get_engine():
	config = get_connection_config()
	return create_engine(f'mysql+mysqldb://{config.get("username")}:{config.get("password")}@{config.get("host")}/mtgdp')
