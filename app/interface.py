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

def show_dashboard(user_name):
    login_frame.pack_forget()
    welcome_label.config(text=f"Bem-vindo, {user_name}")
    dashboard_frame.pack(fill="both", expand=True)

def show_login():
    dashboard_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

def logout():
    try:
        response = session.post(f"{API}/logout")

        if response.status_code == 200:
            messagebox.showinfo("Logout", "Logout realizado com sucesso")
            show_login()
        else:
            messagebox.showerror("Erro", "Falha no Logout")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "API Flask não está rodando")

root.mainloop()
