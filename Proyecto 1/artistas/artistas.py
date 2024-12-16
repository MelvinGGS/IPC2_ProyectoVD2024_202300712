# artist_module.py
import tkinter as tk
from tkinter import messagebox

class ModuloArtista:
    def __init__(self, root):
        self.root = root
        self.root.title("ARTISTAS")
        root.geometry("800x600")
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="Módulo Artistas", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Configurar arte", command=self.gestionar_arte, font=("Helvetica", 16), width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.cerrar_sesion, font=("Helvetica", 16), width=20, height=2).pack(pady=10)

    def gestionar_arte(self):
        messagebox.showinfo("Gestionar Arte", "Funcionalidad de gestión de arte")

    def cerrar_sesion(self):
        self.root.destroy()