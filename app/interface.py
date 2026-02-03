import tkinter as tk
from tkinter import messagebox
import requests

API = "http://127.0.0.1:5000"
session = requests.Session()

root = tk.Tk()

name_entry = tk.Entry(root)
email_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")

root.title("Sistema")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="Nome").pack()
name_entry.pack()

tk.Label(root, text="Email").pack()
email_entry.pack()

tk.Label(root, text="Senha").pack()
password_entry.pack()

def login():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Erro: ", "Email e senha são obrigatórios")
        return

    try:
        response = session.post(
            f"{API}/login",
            json={"email": email, "password": password}
        )
        data = response.json()

        if response.status_code == 200:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {data['user']['name']}")
            logout_btn.config(state="normal")
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
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        data = response.json()

        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso")
        else:
            messagebox.showerror("Erro", data.get("error", "Erro desconhecido"))

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

tk.Button(root, text="Entrar", width=20, command=login).pack(pady=5)
tk.Button(root, text="Cadastrar", width=20, command=register).pack(pady=5)

logout_btn = tk.Button(root, text="Logout", width=20, state="disabled")
logout_btn.pack(pady=5)

def logout():
    try:
        response = session.post(f"{API}/logout")

        if response.status_code == 200:
            messagebox.showinfo("Logout", "Logout realizado com sucesso")
            logout_btn.config(state="disabled")
        else:
            messagebox.showerror("Erro", "Falha no Logout")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")


logout_btn.config(command=logout)

root.mainloop()
