from flask import Blueprint, request, jsonify, session
from db import get_connection
import sqlite3

books_bp = Blueprint("books", __name__)

@books_bp.route("/books", methods=["POST"])
def insert_book():
    if "user_id" not in session:
        return jsonify({"error": "user not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "no body"}), 400

    return validate_book(data)

@books_bp.route("/books", methods=["GET"])
def get_books():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, user_id FROM books")
        books = cursor.fetchall()

    return jsonify([dict(book) for book in books])

@books_bp.route("/books/<int:id>", methods=["PATCH"])
def update_book(id):
    if "user_id" not in session:
        return jsonify({"error": "user not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "no body"}), 400

    fields = []
    values = []

    if "title" in data:
        if not isinstance(data["title"], str):
            return jsonify({"error": "title must be a string"}), 400
        fields.append("title = ?")
        values.append(data["title"])

    if "author" in data:
        if not isinstance(data["author"], str):
            return jsonify({"error": "author must be a string"}), 400
        fields.append("author = ?")
        values.append(data["author"])

    if not fields:
        return jsonify({"error": "no fields to update"}), 400

    values.append(id)
    values.append(session["user_id"])

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE books 
            SET {', '.join(fields)} 
            WHERE id = ? AND user_id = ?
            """,
            tuple(values)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "book not found or not allowed"}), 404

    return jsonify({"message": "Book updated successfully"}), 200

@books_bp.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    with get_connection() as conn:
        cursor = conn.cursor()

        book = cursor.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
        if not book:
            return jsonify({"error" : "book does not exists"}), 404

        conn.execute("DELETE FROM books WHERE id = ?", (id,))
        return jsonify(({"message": "Book deleted successfully"})), 200

def validate_book(book: dict):
    required_fields = ["title", "author"]

    for field in required_fields:
        if field not in book or book[field] is None:
            return jsonify({"error": f"field {field} is required"}), 400

        if not isinstance(book[field], str):
            return jsonify({"error": f"{field} must be a string"}), 400

    user_id = session["user_id"]

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, user_id) VALUES (?, ?, ?)",
                (book["title"], book["author"], user_id)
            )
            book_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        return jsonify({"error": "book already exists"}), 400

    return jsonify({
        "message": "Book created successfully",
        "book": {
            "id": book_id,
            "title": book["title"],
            "author": book["author"],
            "user_id": user_id
        }
    }), 201
