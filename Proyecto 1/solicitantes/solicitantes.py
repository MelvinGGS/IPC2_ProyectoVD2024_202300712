# modulo_solicitantes.py
import tkinter as tk
from tkinter import messagebox

class ModuloSolicitantes:
    def __init__(self, root, lista_artistas=None, lista_solicitantes=None):
        self.root = root
        self.root.title("SOLICITANTES")
        root.geometry("1400x725")
        # Guardar referencia a las listas
        self.lista_artistas = lista_artistas
        self.lista_solicitantes = lista_solicitantes
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="Módulo solicitantes", font=("Helvetica", 16)).pack(pady=2)
        
        # Marco para botones horizontales
        marco_botones = tk.Frame(self.root)
        marco_botones.pack(pady=1)
        
        # Crear 6 botones en línea horizontal
        tk.Button(marco_botones, text="Cargar figura", command=self.ver_artistas,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Solicitar", command=self.aplicar_proyecto,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Ver pila", command=self.ver_aplicaciones,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Ver lista", command=self.ver_perfil,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Imágenes", command=self.modificar_perfil,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Cerrar Sesión", command=self.cerrar_sesion,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)

    def ver_artistas(self):
        messagebox.showinfo("Info", "Cargar figura a graficar")

    def aplicar_proyecto(self):
        messagebox.showinfo("Info", "Solicitar figura")

    def ver_aplicaciones(self):
        messagebox.showinfo("Info", "Ver pila de solicitudes")

    def ver_perfil(self):
        messagebox.showinfo("Info", "Ver lista de solicitudes")

    def modificar_perfil(self):
        messagebox.showinfo("Info", "Ver todas las imágenes")

    def cerrar_sesion(self):
        ventana_login = tk.Tk()
        from login import LoginWindow
        app = LoginWindow(ventana_login, self.lista_artistas, self.lista_solicitantes)
        self.root.destroy()
        ventana_login.mainloop()