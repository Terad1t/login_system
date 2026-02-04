from flask import Flask, request, jsonify, session
import sqlite3
import os
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from books import books_bp

app = Flask(__name__)
app.secret_key= os.urandom(24)
app.register_blueprint(books_bp)

@app.route("/users", methods=["POST"])
def insert_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no body"}), 400

    return validar_user(data)

@app.route("/users", methods=["GET"])
def get_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()

        return jsonify([dict(user) for user in users])

@app.route("/users", methods=["PATCH"])
def update_user():
    if "user_id" not in session:
        return jsonify({"error": "user not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "no body"}), 400

    fields = []
    values = []

    if "name" in data:
        fields.append("name = ?")
        values.append(data["name"])

    if "email" in data:
        if "@" not in data["email"] or "." not in data["email"]:
            return jsonify({"error": "invalid email"}), 400
        fields.append("email = ?")
        values.append(data["email"])

    if "password" in data:
        if len(data["password"]) < 8:
            return jsonify({"error": "password must be at least 8 characters"}), 400
        password_hash = generate_password_hash(data["password"])
        fields.append("password = ?")
        values.append(password_hash)

    if not fields:
        return jsonify({"error": "no fields to update"}), 400

    values.append(session["user_id"])

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET {', '.join(fields)} WHERE id = ?",
            tuple(values)
        )

    return jsonify({"message": "User updated successfully"}), 200


@app.route("/users/<int:id>", methods=["DELETE"])
def remove_user(id):
    with get_connection() as conn:
        cursor = conn.cursor()

        user = cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
        if not user:
            return jsonify({"error": "user does not exist"}), 404

        conn.execute("DELETE FROM users WHERE id = ?", (id,))
        return jsonify({"message": "User deleted successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no body"}), 400

    email = data["email"]
    password = data["password"]

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "user does not exist"}), 400

        if not check_password_hash(user["password"], password):
            return jsonify({"error": "wrong password"}), 400

        session["user_id"] = user["id"]

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

@app.route("/me", methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"error": "user not logged in"}), 401

    return jsonify({"message" : "You are logged in"}), 200

@app.route("/logout", methods=["POST"])
def logout_user():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

def validar_user(user: dict):
    required_fields = ["name", "email", "password"]

    for field in required_fields:
        if field not in user or user[field] is None:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    if not isinstance(user["name"], str):
        return jsonify({"error": "name must be a string"}), 400

    if not isinstance(user["email"], str):
        return jsonify({"error": "email must be a string"}), 400

    if not isinstance(user["password"], str):
        return jsonify({"error": "password must be a string"}), 400

    if len(user["password"]) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400

    if "@" not in user["email"] or "." not in user["email"]:
        return jsonify({"error": "invalid email"}), 400

    password_hash = generate_password_hash(user["password"])

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (user["name"], user["email"], password_hash)
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
