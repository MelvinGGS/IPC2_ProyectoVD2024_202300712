# artist_module.py
import tkinter as tk
from tkinter import messagebox

class ModuloArtista:
    def __init__(self, root, lista_artistas=None, lista_solicitantes=None):
        self.root = root
        self.root.title("ARTISTAS")
        root.geometry("1400x725")
        # Guardar referencia a las listas
        self.lista_artistas = lista_artistas
        self.lista_solicitantes = lista_solicitantes
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="Módulo Artistas", font=("Helvetica", 16)).pack(pady=2)
        
        # Marco para botones horizontales
        marco_botones = tk.Frame(self.root)
        marco_botones.pack(pady=1)
        
        # Crear 4 botones en línea horizontal
        tk.Button(marco_botones, text="Aceptar", command=self.ver_solicitudes,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Ver cola", command=self.ver_perfil,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Imágenes solicitadas", command=self.modificar_perfil,
                 font=("Helvetica", 12), width=20, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Cerrar Sesión", command=self.cerrar_sesion,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)

    def ver_solicitudes(self):
        messagebox.showinfo("Info", "Aceptar solicitudes")

    def ver_perfil(self):
        messagebox.showinfo("Info", "Ver cola de solicitudes")

    def modificar_perfil(self):
        messagebox.showinfo("Info", "Ver imágenes solicitadas")

    def cerrar_sesion(self):
        ventana_login = tk.Tk()
        from login import LoginWindow
        app = LoginWindow(ventana_login, self.lista_artistas, self.lista_solicitantes)
        self.root.destroy()
        ventana_login.mainloop()