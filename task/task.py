
from flask import jsonify, request
from psycopg2 import extras
from cryptography.fernet import Fernet

from db import db

def get_tasks():
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)


def create_task():
    new_task = request.get_json()
    title = new_task['title']
    user_id = new_task['user_id']
    is_open = True

    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO tasks (title, user_id, is_open) VALUES (%s, %s, %s) RETURNING *",
                (title, user_id, is_open))
    new_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_task)


def get_task(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cur.fetchone()
    cur.close()
    conn.close()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify(task)


def update_task(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_task = request.get_json()
    title = new_task['title']
    is_open = new_task['is_open']
    cur.execute("UPDATE tasks SET title = %s, is_open = %s WHERE id = %s RETURNING *",
                (title, is_open, id))
    updated_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if updated_task is None:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(updated_task)


def delete_task(id):
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING *", (id,))
    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(task)