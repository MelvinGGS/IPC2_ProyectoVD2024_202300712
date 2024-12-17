# login.py
import tkinter as tk
from tkinter import messagebox
from admin.admin import ModuloAdmin  # Import ModuloAdmin
from artistas.artistas import ModuloArtista  # Import ModuloArtista
from solicitantes.solicitantes import ModuloSolicitantes  # Import ModuloSolicitantes
from models.linked_list import ListaDoblementeEnlazada
from models.simple_list import ListaSimple

class LoginWindow:
    def __init__(self, root, lista_artistas=None, lista_solicitantes=None):
        self.root = root
        self.root.title("Inicio de Sesión - IPCArt-Studio")
        self.root.geometry("800x600")
        
        # Usar las listas existentes o crear nuevas si no se proporcionan
        self.lista_artistas = lista_artistas if lista_artistas is not None else ListaSimple()
        self.lista_solicitantes = lista_solicitantes if lista_solicitantes is not None else ListaDoblementeEnlazada()
        
        self.crear_widgets()
    
    def crear_widgets(self):
        tk.Label(self.root, text="Nombre de usuario", font=("Helvetica", 30)).pack(pady=20)
        self.entrada_usuario = tk.Entry(self.root, width=90, font=("Helvetica", 10))
        self.entrada_usuario.pack(ipady=10, pady=10)
        
        tk.Label(self.root, text="Contraseña", font=("Helvetica", 30)).pack(pady=20)
        self.entrada_contrasena = tk.Entry(self.root, show="*", width=90, font=("Helvetica", 10))
        self.entrada_contrasena.pack(ipady=10, pady=10)
        
        tk.Button(self.root, text="INGRESAR", command=self.iniciar_sesion, 
                 font=("Helvetica", 20), width=20, height=2).pack(pady=20)

    def validar_usuario(self, usuario, contrasena):
        if usuario == "AdminIPC" and contrasena == "ARTIPC2":
            return "admin"
        
        actual = self.lista_artistas.primero
        while actual:
            if actual.valor['id'] == usuario and actual.valor['pwd'] == contrasena:
                return "artista"
            actual = actual.siguiente
        
        actual = self.lista_solicitantes.primero
        while actual:
            if actual.valor['id'] == usuario and actual.valor['pwd'] == contrasena:
                return "solicitante"
            actual = actual.siguiente
        
        return None

    def iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()
        
        tipo_usuario = self.validar_usuario(usuario, contrasena)
        
        if tipo_usuario == "admin":
            self.root.destroy()
            ventana_admin = tk.Tk()
            admin = ModuloAdmin(ventana_admin)
            self.lista_artistas = admin.artistas
            self.lista_solicitantes = admin.solicitantes
            ventana_admin.mainloop()
        elif tipo_usuario == "artista":
            self.root.destroy()
            ventana_artista = tk.Tk()
            modulo = ModuloArtista(ventana_artista, self.lista_artistas, self.lista_solicitantes)
            modulo.id_artista = usuario  # Aquí se establece el ID del artista
            ventana_artista.mainloop()
        elif tipo_usuario == "solicitante":
            self.root.destroy()
            ventana_solicitante = tk.Tk()
            modulo = ModuloSolicitantes(ventana_solicitante, self.lista_artistas, self.lista_solicitantes)
            modulo.id_solicitante = usuario  # Store the user ID
            ventana_solicitante.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# main.py
import tkinter as tk
from login import LoginWindow

def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()