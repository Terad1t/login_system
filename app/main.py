from flask import Flask, request, jsonify
import sqlite3
from db import get_connection

app = Flask(__name__)

@app.route("/", methods=["POST"])
def insert_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no body"}), 400

    return validar_user(data)

@app.route("/users", methods=["GET"])
def get_users():
    users = get_connection().execute(
        "SELECT * FROM users"
    ).fetchall()


def validar_user(user: dict):
    required_fields = ["name", "email"]

    for field in required_fields:
        if field not in user or user[field] is None:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    if not isinstance(user["name"], str):
        return jsonify({"error": "name must be a string"}), 400

    if not isinstance(user["email"], str):
        return jsonify({"error": "email must be a string"}), 400

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (user["name"], user["email"])
            )
            user_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        return jsonify({"error": "user already exists"}), 409

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": user_id,
            "name": user["name"],
            "email": user["email"]
        }
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
