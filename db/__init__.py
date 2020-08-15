from sqlalchemy import create_engine
import sqlalchemy
import MySQLdb
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
DB_NAME = 'mtgdp'


def get_connection_config():
	with open('credentials/db.json', 'r') as f:
		config = json.loads(f.read())
	return config


def get_engine():
	config = get_connection_config()
	connection_str = f'mysql+mysqldb://{config.get("username")}:{config.get("password")}@{config.get("host")}/{DB_NAME}'
	return create_engine(connection_str)


def get_session() -> sqlalchemy.orm.session.Session:
	Session = sessionmaker(bind=get_engine())
	return Session()
