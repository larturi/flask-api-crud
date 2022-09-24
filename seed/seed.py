
from flask import jsonify
from psycopg2 import extras
from db import db

def create_tables():
    drop_all_tables()
    create_user_table()
    create_task_table()
    return jsonify({"message": "Tables created successfully"})


def drop_all_tables():
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""DROP TABLE users, tasks;""")
    conn.commit()
    cur.close()
    conn.close()
    
    
def create_user_table():
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );""")
    conn.commit()
    cur.close()
    conn.close()
    
    
def create_task_table():
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    user_id SERIAL NOT NULL,
                    is_open BOOLEAN NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_user
                        FOREIGN KEY(user_id) 
                            REFERENCES users(id)
                );""")
    conn.commit()
    cur.close()
    conn.close()