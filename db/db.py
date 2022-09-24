from flask import Flask
from psycopg2 import connect
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
key = Fernet.generate_key()

host = environ.get('POSTGRES_HOST')
database = environ.get('POSTGRES_DB')
username = environ.get('POSTGRES_USER')
password = environ.get('POSTGRES_PASSWORD')
port = environ.get('DB_PORT')

def db_connection():
    conn = connect(host=host, port=port, dbname=database, user=username,password=password)
    return conn