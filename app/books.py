from flask import Blueprint, request, jsonify, session
from db import get_connection
import sqlite3
from werkzeug.security import check_password_hash

books_bp = Blueprint("books", __name__)

# Criar um livro
@books_bp.route("/books", methods=["POST"])
def insert_book():
    if "user_id" not in session:
        return jsonify({"error": "user not logged in"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "no body"}), 400

    return validate_book(data)

# Listar todos os livros
@books_bp.route("/books", methods=["GET"])
def get_books():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, user_id FROM books")
        books = cursor.fetchall()

    return jsonify([dict(book) for book in books])

# Função de validação e inserção
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
