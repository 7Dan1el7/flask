from flask import Flask, request, jsonify, render_template
import psycopg
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Створення таблиці
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER
    );
""")
conn.commit()


# ----------------------------- HTML сторінки -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def users_page():
    return render_template("users.html")


# ----------------------------- API: CREATE -----------------------------
@app.route("/api/data", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    age = data.get("age")

    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()

    return jsonify({"status": "success"})


# ----------------------------- API: READ -----------------------------
@app.route("/api/users", methods=["GET"])
def get_users():
    cursor.execute("SELECT id, name, age FROM users;")
    users = cursor.fetchall()

    return jsonify([
        {"id": u[0], "name": u[1], "age": u[2]} for u in users
    ])


# ----------------------------- API: UPDATE -----------------------------
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    age = data.get("age")

    cursor.execute(
        "UPDATE users SET name=%s, age=%s WHERE id=%s",
        (name, age, user_id)
    )
    conn.commit()

    return jsonify({"status": "updated"})


# ----------------------------- API: DELETE -----------------------------
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()

    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
