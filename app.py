from flask import Flask, request, jsonify
import os
import psycopg

app = Flask(__name__)

# Підключення до бази (psycopg3)
def get_db_connection():
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    return conn


@app.route("/")
def home():
    return "Сервер працює! PostgreSQL підключено ✔"


@app.route("/create_table")
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INTEGER
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    return "Таблиця users створена ✔"


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data["name"]
    age = data["age"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, age) VALUES (%s, %s);",
        (name, age)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "message": "Користувача додано"})


@app.route("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    users = [{"id": r[0], "name": r[1], "age": r[2]} for r in rows]
    cur.close()
    conn.close()
    return jsonify(users)


@app.route("/api/data", methods=["POST"])
def handle_data():
    data = request.json
    return jsonify({
        "message": f"Привіт, {data['name']}! Тобі {data['age']} років.",
        "status": "success"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0")
