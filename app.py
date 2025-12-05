from flask import Flask, request, jsonify

app = Flask(__name__)

# Головна сторінка
@app.route("/")
def home():
    return "Сервер працює! Готовий приймати дані"

# Обробка POST-запиту
@app.route("/api/data", methods=["POST"])
def handle_data():
    data = request.json  # Отримати JSON від користувача

    # Наприклад: data = {"name": "Tom", "age": 20}
    name = data.get("name")
    age = data.get("age")

    # Обробка (тут просто формуємо відповідь)
    response = {
        "message": f"Привіт, {name}! Тобі {age} років.",
        "status": "success"
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
