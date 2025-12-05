from flask import Flask, request, jsonify, render_template, redirect
import os
import psycopg

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")


# --- Підключення до БД ---
def get_connection():
    return psycopg.connect(DATABASE_URL)


# --- Головна сторінка (форма додавання користувача) ---
@app.route("/")
def index():
    return render_template("index.html")


# --- Створення запису (C in CRUD) ---
@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    age = data.get("age")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, age) VALUES (%s, %s)",
                (name, age)
            )

    return jsonify({"status": "success", "message": "Користувача додано"})


# --- Отримати всіх користувачів (R in CRUD) ---
@app.route("/api/users", methods=["GET"])
def get_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, age FROM users ORDER BY id")
            rows = cur.fetchall()

    users = [{"id": r[0], "name": r[1], "age": r[2]} for r in rows]
    return jsonify(users)


# --- Оновлення (U in CRUD) ---
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    age = data.get("age")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name=%s, age=%s WHERE id=%s",
                (name, age, user_id)
            )

    return jsonify({"status": "success", "message": "Користувача оновлено"})


# --- Видалення (D in CRUD) ---
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))

    return jsonify({"status": "success", "message": "Користувача видалено"})


# --- Сторінка зі списком ---
@app.route("/users")
def users_page():
    return render_template("users.html")


# --- Створення таблиці 1 раз ---
@app.route("/create_table")
def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    age INT
                );
            """)

    return "Таблиця users створена ✔"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
