# applicant_module.py
import tkinter as tk
from tkinter import messagebox

class ApplicantModule:
    def __init__(self, root):
        self.root = root
        self.root.title("SOLICITANTES")
        root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Modulo solicitantes", font=("Helvetica", 16)).pack(pady=20)  # Increase font size and add padding
        tk.Button(self.root, text="Aplicar", command=self.apply, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding
        tk.Button(self.root, text="Salir", command=self.logout, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding

    def apply(self):
        # ...existing code...
        messagebox.showinfo("Apply", "Application functionality")

    def logout(self):
        # ...existing code...
        self.root.destroy()
        # main function is not defined, so we remove the call