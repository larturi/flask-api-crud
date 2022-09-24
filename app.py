from flask import Flask, jsonify, request
from psycopg2 import connect, extras
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv

from seed import seed
from user import user

load_dotenv()

app = Flask(__name__)

# Seed Routes
@app.get('/api/seed')
def create_tables(): return seed.create_tables();


# User Routes
@app.get('/api/users')
def get_users(): return user.get_users()

@app.post('/api/users')
def create_user(): return user.create_user()

@app.get('/api/users/<id>')
def get_user(id): return user.get_user(id)

@app.put('/api/users/<id>')
def update_user(id): return user.update_user(id)

@app.delete('/api/users/<id>')
def delete_user(id): return user.delete_user(id)


if __name__ == '__main__':
    app.run(debug=True)