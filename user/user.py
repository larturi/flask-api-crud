
from flask import jsonify, request
from psycopg2 import extras
from cryptography.fernet import Fernet

from db import db

key = Fernet.generate_key()

def get_users():
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT u.id, u.username, u.email FROM users u")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


def create_user():
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *",
                (username, email, password))
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_user)


def get_user(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)


def update_user(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    cur.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *",
                (username, email, password, id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if updated_user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(updated_user)


def delete_user(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


def get_users_tasks(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""SELECT u.id as user_id, t.title, t.is_open, t.created_at
                   FROM users u 
                   INNER JOIN tasks t ON u.id = t.user_id
                   ORDER BY t.created_at DESC
                """)
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)