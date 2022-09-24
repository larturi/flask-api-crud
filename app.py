from flask import Flask, jsonify, request
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

app = Flask(__name__)

key = Fernet.generate_key()

host = "localhost"
port = "5432"
dbname = "flask-crud"
user = "flask"
password = "flask"

def db_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user,password=password)
    return conn

@app.get('/api/seed')
def create_tables():
    conn = db_connection()
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


@app.get('/api/users')
def get_users():
    conn = db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    conn = db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *",
                (username, email, password))
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_user)


@app.get('/api/users/<id>')
def get_user(id):
    conn = db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)