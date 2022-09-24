from flask import Flask, jsonify, request
from psycopg2 import connect, extras
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv

from seed import seed
from user import user
from task import task

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

@app.get('/api/users/tasks/<id>')
def get_users_tasks(id): return user.get_users_tasks(id)


# Task Routes
@app.get('/api/tasks')
def get_tasks(): return task.get_tasks()

@app.post('/api/tasks')
def create_task(): return task.create_task()

@app.get('/api/tasks/<id>')
def get_task(id): return task.get_task(id)

@app.put('/api/tasks/<id>')
def update_task(id): return task.update_task(id)

@app.delete('/api/tasks/<id>')
def delete_task(id): return task.delete_task(id)


if __name__ == '__main__':
    app.run(debug=True)