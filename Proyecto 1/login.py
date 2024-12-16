# login.py
import tkinter as tk
from tkinter import messagebox
from admin.admin import ModuloAdmin  # Import ModuloAdmin
from artistas.artistas import ModuloArtista  # Import ModuloArtista
from solicitantes.solicitantes import ModuloSolicitantes  # Import ModuloSolicitantes

def iniciar_sesion():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    if usuario == "A" and contrasena == "A":
        root.destroy()
        ventana_admin = tk.Tk()
        ModuloAdmin(ventana_admin)
        ventana_admin.mainloop()
    elif usuario == "artista" and contrasena == "artista":
        root.destroy()
        ventana_artista = tk.Tk()
        ModuloArtista(ventana_artista)
        ventana_artista.mainloop()
    elif usuario == "soli" and contrasena == "soli":
        root.destroy()
        ventana_solicitante = tk.Tk()
        ModuloSolicitantes(ventana_solicitante)
        ventana_solicitante.mainloop()
    else:
        messagebox.showerror("Error de inicio de sesión", "Datos incorrectos")

root = tk.Tk()
root.title("Inicio de Sesión - IPCArt-Studio")
root.geometry("800x600")

tk.Label(root, text="Nombre de usuario", font=("Helvetica", 30)).pack(pady=20)  # Increase font size and add padding
entrada_usuario = tk.Entry(root, width=90, font=("Helvetica", 10))  # Increase font size
entrada_usuario.pack(ipady=10, pady=10)  # Increase height and add padding

tk.Label(root, text="Contraseña", font=("Helvetica", 30)).pack(pady=20)  # Increase font size and add padding
entrada_contrasena = tk.Entry(root, show="*", width=90, font=("Helvetica", 10))  # Increase font size
entrada_contrasena.pack(ipady=10, pady=10)  # Increase height and add padding

tk.Button(root, text="INGRESAR", command=iniciar_sesion, font=("Helvetica", 20), width=20, height=2).pack(pady=20)  # Increase size and add padding

root.mainloop()

# main.py
import tkinter as tk
from login import iniciar_sesion

def main():
    root = tk.Tk()
    iniciar_sesion()
    root.mainloop()

if __name__ == "__main__":
    main()