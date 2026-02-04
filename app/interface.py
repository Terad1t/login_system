import tkinter as tk
from tkinter import messagebox
import requests

API = "http://127.0.0.1:5000"
session = requests.Session()

root = tk.Tk()
root.title("Sistema")
root.geometry("400x350")
root.resizable(False, False)

login_frame = tk.Frame(root)
dashboard_frame = tk.Frame(root)

login_frame.pack(fill="both", expand=True)

name_entry = tk.Entry(login_frame)
email_entry = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame, show="*")

tk.Label(login_frame, text="Nome").pack()
name_entry.pack()

tk.Label(login_frame, text="Email").pack()
email_entry.pack()

tk.Label(login_frame, text="Senha").pack()
password_entry.pack()

def login():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Erro", "Email e senha são obrigatórios")
        return

    try:
        response = session.post(
            f"{API}/login",
            json={"email": email, "password": password}
        )
        data = response.json()

        if response.status_code == 200:
            show_dashboard(data["user"]["name"])
        else:
            messagebox.showerror("Erro", data.get("error", "Erro desconhecido"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

def register():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not name or not email or not password:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    try:
        response = requests.post(
            f"{API}/users",
            json={"name": name, "email": email, "password": password}
        )

        data = response.json()

        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso")
        else:
            messagebox.showerror("Erro", data.get("error", "Erro desconhecido"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

tk.Button(login_frame, text="Entrar", width=20, command=login).pack(pady=5)
tk.Button(login_frame, text="Cadastrar", width=20, command=register).pack(pady=5)

welcome_label = tk.Label(dashboard_frame, text="", font=("Arial", 14))
welcome_label.pack(pady=20)

tk.Button(
    dashboard_frame,
    text="Logout",
    width=20,
    command=lambda: logout()
).pack()

def show_login():
    dashboard_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

tk.Label(dashboard_frame, text="Título do livro").pack()
book_title_entry = tk.Entry(dashboard_frame)
book_title_entry.pack()

tk.Label(dashboard_frame, text="Autor").pack()
book_author_entry = tk.Entry(dashboard_frame)
book_author_entry.pack()

# --- BOOK LIST ---
books_listbox = tk.Listbox(dashboard_frame, width=45)
books_listbox.pack(pady=10)

def load_books():
    books_listbox.delete(0, tk.END)

    try:
        response = session.get(f"{API}/books")
        if response.status_code == 200:
            for book in response.json():
                books_listbox.insert(
                    tk.END,
                    f"{book['id']} - {book['title']} ({book['author']})"
                )
        else:
            messagebox.showerror("Erro", "Erro ao carregar livros")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

def show_dashboard(user_name):
    login_frame.pack_forget()
    welcome_label.config(text=f"Bem-vindo, {user_name}")
    dashboard_frame.pack(fill="both", expand=True)
    load_books()

def create_book():
    title = book_title_entry.get()
    author = book_author_entry.get()

    if not title or not author:
        messagebox.showerror("Erro", "Título e autor são obrigatórios")
        return

    try:
        response = session.post(
            f"{API}/books",
            json={"title": title, "author": author}
        )

        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Livro criado com sucesso")
            book_title_entry.delete(0, tk.END)
            book_author_entry.delete(0, tk.END)
            load_books()
        else:
            messagebox.showerror("Erro", response.json().get("error"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

tk.Button(dashboard_frame, text="Criar Livro", command=create_book).pack(pady=5)

def on_book_select(event):
    selection = books_listbox.curselection()
    if not selection:
        return

    text = books_listbox.get(selection[0])
    _, rest = text.split(" - ", 1)
    title, author = rest.rsplit(" (", 1)
    author = author.replace(")", "")

    book_title_entry.delete(0, tk.END)
    book_author_entry.delete(0, tk.END)
    book_title_entry.insert(0, title)
    book_author_entry.insert(0, author)

books_listbox.bind("<<ListboxSelect>>", on_book_select)


def update_book():
    selection = books_listbox.curselection()
    if not selection:
        messagebox.showerror("Erro", "Selecione um livro")
        return

    book_id = books_listbox.get(selection[0]).split(" - ")[0]
    title = book_title_entry.get()
    author = book_author_entry.get()

    data = {}
    if title:
        data["title"] = title
    if author:
        data["author"] = author

    if not data:
        messagebox.showerror("Erro", "Informe algo para atualizar")
        return

    try:
        response = session.patch(f"{API}/books/{book_id}", json=data)

        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Livro atualizado")
            load_books()
        else:
            messagebox.showerror("Erro", response.json().get("error"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

tk.Button(dashboard_frame, text="Atualizar Livro", command=update_book).pack(pady=5)

def delete_book():
    selection = books_listbox.curselection()
    if not selection:
        messagebox.showerror("Erro", "Selecione um livro")
        return

    book_id = books_listbox.get(selection[0]).split(" - ")[0]

    if not messagebox.askyesno("Confirmação", "Deseja deletar o livro?"):
        return

    try:
        response = session.delete(f"{API}/books/{book_id}")

        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Livro deletado")
            load_books()
        else:
            messagebox.showerror("Erro", response.json().get("error"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

tk.Button(dashboard_frame, text="Deletar Livro", command=delete_book).pack(pady=5)

def logout():
    try:
        response = session.post(f"{API}/logout")

        if response.status_code == 200:
            books_listbox.delete(0, tk.END)
            show_login()
            messagebox.showinfo("Logout", "Logout realizado com sucesso")
        else:
            messagebox.showerror("Erro", "Falha no Logout")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")


root.mainloop()
