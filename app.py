from flask import Flask, request, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ФУНКЦІЯ ПІДКЛЮЧЕННЯ ДО БАЗИ
def get_db_connection():
    # DATABASE_URL автоматично підставляється Railway
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    return conn


# Головна сторінка
@app.route("/")
def home():
    return "Сервер працює! База даних підключена ✔️"


# --- СТВОРЕННЯ ТАБЛИЦІ ---
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
    return "Таблиця users створена ✔️"


# --- ДОДАВАННЯ КОРИСТУВАЧА ---
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


# --- ОТРИМАННЯ ВСІХ КОРИСТУВАЧІВ ---
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


# --- ТВОЄ ТЕСТОВЕ API /api/data — залишаю теж ---
@app.route("/api/data", methods=["POST"])
def handle_data():
    data = request.json
    name = data.get("name")
    age = data.get("age")

    response = {
        "message": f"Привіт, {name}! Тобі {age} років.",
        "status": "success"
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
