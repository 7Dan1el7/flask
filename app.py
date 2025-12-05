from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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
