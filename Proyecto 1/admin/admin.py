# admin_module.py
import tkinter as tk
from tkinter import messagebox

class AdminModule:
    def __init__(self, root):
        self.root = root
        self.root.title("ADMINISTRADOR")
        root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Modulo administrador", font=("Helvetica", 16)).pack(pady=20)  # Increase font size and add padding
        tk.Button(self.root, text="Usuarios", command=self.manage_users, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding
        tk.Button(self.root, text="Contenido", command=self.manage_content, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding
        tk.Button(self.root, text="Salir", command=self.logout, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding

    def manage_users(self):
        # ...existing code...
        messagebox.showinfo("Manage Users", "User management functionality")

    def manage_content(self):
        # ...existing code...
        messagebox.showinfo("Manage Content", "Content management functionality")

    def logout(self):
        # ...existing code...
        self.root.destroy()
        # main function is not defined, so we remove the call