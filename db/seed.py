from flask import Flask, jsonify
from psycopg2 import connect, extras

app = Flask(__name__)

host = "localhost"
port = "5432"
dbname = "flask-crud"
user = "flask"
password = "flask"

def db_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user,password=password)
    return conn

