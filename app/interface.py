import requests
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from ttkbootstrap.widgets.tableview import Tableview


API = "http://127.0.0.1:5000"
session = requests.Session()

root = tb.Window(
    title="Sistema de Livros",
    themename="darkly",
    size=(450, 520),
    resizable=(False, False)
)

login_frame = tb.Frame(root, padding=25)
dashboard_frame = tb.Frame(root, padding=20)

login_frame.pack(fill=BOTH, expand=YES)

tb.Label(
    login_frame,
    text="Login",
    font=("Segoe UI", 20, "bold")
).grid(row=0, column=0, columnspan=2, pady=(0, 20))

tb.Label(login_frame, text="Nome").grid(row=1, column=0, sticky=W)
name_entry = tb.Entry(login_frame, width=30)
name_entry.grid(row=1, column=1, pady=5)

tb.Label(login_frame, text="Email").grid(row=2, column=0, sticky=W)
email_entry = tb.Entry(login_frame, width=30)
email_entry.grid(row=2, column=1, pady=5)

tb.Label(login_frame, text="Senha").grid(row=3, column=0, sticky=W)
password_entry = tb.Entry(login_frame, width=30, show="*")
password_entry.grid(row=3, column=1, pady=5)

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

        if response.status_code == 200:
            show_dashboard(response.json()["user"]["name"])
        else:
            messagebox.showerror("Erro", response.json().get("error"))

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
        response = session.post(
            f"{API}/users",
            json={"name": name, "email": email, "password": password}
        )

        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso")
        else:
            messagebox.showerror("Erro", response.json().get("error"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

tb.Button(
    login_frame,
    text="Entrar",
    bootstyle=SUCCESS,
    width=30,
    command=login
).grid(row=4, column=0, columnspan=2, pady=(20, 5))

tb.Button(
    login_frame,
    text="Cadastrar",
    bootstyle=PRIMARY,
    width=30,
    command=register
).grid(row=5, column=0, columnspan=2)

welcome_label = tb.Label(
    dashboard_frame,
    text="",
    font=("Segoe UI", 16, "bold")
)
welcome_label.pack(pady=(0, 15))

tb.Label(dashboard_frame, text="Título do Livro").pack(anchor=W)
book_title_entry = tb.Entry(dashboard_frame, width=40)
book_title_entry.pack(pady=3)

tb.Label(dashboard_frame, text="Autor").pack(anchor=W)
book_author_entry = tb.Entry(dashboard_frame, width=40)
book_author_entry.pack(pady=3)

books_listbox = Tableview(
    master=dashboard_frame,
    coldata=[
        {"text": "ID", "stretch": False},
        {"text": "Título", "stretch": True},
        {"text": "Autor", "stretch": True},
    ],
    rowdata=[],
    paginated=False,
    searchable=False,
    height=8,
    bootstyle=PRIMARY
)

books_listbox.pack(fill=BOTH, expand=YES, pady=10)

def load_books():
    # remove todas as linhas corretamente
    for row in books_listbox.get_rows():
        books_listbox.delete_row(row.iid)

    try:
        response = session.get(f"{API}/books")

        if response.status_code == 200:
            for book in response.json():
                books_listbox.insert_row(
                    "end",
                    [book["id"], book["title"], book["author"]]
                )
        else:
            messagebox.showerror("Erro", "Erro ao carregar livros")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")


def show_dashboard(user_name):
    login_frame.pack_forget()
    welcome_label.config(text=f"Bem-vindo, {user_name}")
    dashboard_frame.pack(fill=BOTH, expand=YES)
    load_books()

def show_login():
    dashboard_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=YES)

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
            book_title_entry.delete(0, END)
            book_author_entry.delete(0, END)
            load_books()
        else:
            messagebox.showerror("Erro", response.json().get("error"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

def on_book_select(event):
    selected = books_listbox.get_selected_rows()

    if not selected:
        return

    row = selected[0].values
    book_id, title, author = row

    book_title_entry.delete(0, END)
    book_author_entry.delete(0, END)

    book_title_entry.insert(0, title)
    book_author_entry.insert(0, author)


books_listbox.view.bind("<<TreeviewSelect>>", on_book_select)

def update_book():
    selected = books_listbox.get_selected_rows()

    if not selected:
        messagebox.showerror("Erro", "Selecione um livro")
        return

    book_id = selected[0].values[0]

    data = {}
    if book_title_entry.get():
        data["title"] = book_title_entry.get()
    if book_author_entry.get():
        data["author"] = book_author_entry.get()

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


def delete_book():
    selected = books_listbox.get_selected_rows()

    if not selected:
        messagebox.showerror("Erro", "Selecione um livro")
        return

    book_id = selected[0].values[0]

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


def logout():
    try:
        response = session.post(f"{API}/logout")

        if response.status_code == 200:
            for row in books_listbox.get_rows():
                books_listbox.delete_row(row.iid)

            show_login()
            messagebox.showinfo("Logout", "Logout realizado com sucesso")
        else:
            messagebox.showerror("Erro", "Falha no logout")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")


tb.Button(dashboard_frame, text="Criar Livro", bootstyle=SUCCESS, command=create_book).pack(pady=3)
tb.Button(dashboard_frame, text="Atualizar Livro", bootstyle=WARNING, command=update_book).pack(pady=3)
tb.Button(dashboard_frame, text="Deletar Livro", bootstyle=DANGER, command=delete_book).pack(pady=3)
tb.Button(dashboard_frame, text="Logout", bootstyle=SECONDARY, command=logout).pack(pady=10)

root.mainloop()
