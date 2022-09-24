
from flask import jsonify
from psycopg2 import extras
from db import db

def create_tables():
    conn = db.db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);""")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Tables created successfully"})

