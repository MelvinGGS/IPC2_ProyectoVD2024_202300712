# modulo_solicitantes.py
import tkinter as tk
from tkinter import messagebox

class ModuloSolicitantes:
    def __init__(self, root):
        self.root = root
        self.root.title("SOLICITANTES")
        root.geometry("800x600")
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="Módulo solicitantes", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Aplicar", command=self.aplicar, font=("Helvetica", 16), width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.cerrar_sesion, font=("Helvetica", 16), width=20, height=2).pack(pady=10)

    def aplicar(self):
        # ...existing code...
        messagebox.showinfo("Aplicar", "Funcionalidad de aplicación")

    def cerrar_sesion(self):
        # ...existing code...
        self.root.destroy()