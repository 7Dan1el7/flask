from flask import Flask, request, jsonify
import os
import psycopg

app = Flask(__name__)

# ====== Підключення до бази (psycopg3) ======
def get_db_connection():
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    return conn


# ====== ГОЛОВНА ======
@app.route("/")
def home():
    return "Сервер працює! PostgreSQL підключено ✔"


# ====== CREATE TABLE ======
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


# ====== CREATE USER ======
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data["name"]
    age = data["age"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s);", (name, age))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "message": "Користувача додано"})


# ====== READ ALL USERS ======
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [{"id": r[0], "name": r[1], "age": r[2]} for r in rows]

    return jsonify(users)


# ====== READ ONE USER ======
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return jsonify({"id": row[0], "name": row[1], "age": row[2]})
    else:
        return jsonify({"error": "Користувача не знайдено"}), 404


# ====== UPDATE USER ======
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    age = data.get("age")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users 
        SET name = %s, age = %s
        WHERE id = %s;
    """, (name, age, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "message": "Дані оновлено"})


# ====== DELETE USER ======
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "message": "Користувача видалено"})


# ====== ТВОЄ ТЕСТОВЕ API (/api/data) ======
@app.route("/api/data", methods=["POST"])
def handle_data():
    data = request.json
    return jsonify({
        "message": f"Привіт, {data['name']}! Тобі {data['age']} років.",
        "status": "success"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0")
