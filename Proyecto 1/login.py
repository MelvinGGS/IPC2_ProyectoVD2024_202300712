# login.py
import tkinter as tk
from tkinter import messagebox
from admin.admin import AdminModule  # Import AdminModule
from artistas.artistas import ArtistModule  # Import ArtistModule
from solicitantes.solicitantes import ApplicantModule  # Import ApplicantModule

def login():
    username = entry_username.get()
    password = entry_password.get()
<<<<<<< Updated upstream
    if username == "admin" and password == "admin":
=======
    if username == "A" and password == "A":
>>>>>>> Stashed changes
        root.destroy()
        admin_root = tk.Tk()
        AdminModule(admin_root)
        admin_root.mainloop()
    elif username == "artista" and password == "artista":
        root.destroy()
        artist_root = tk.Tk()
        ArtistModule(artist_root)
        artist_root.mainloop()
    elif username == "soli" and password == "soli":
        root.destroy()
        applicant_root = tk.Tk()
        ApplicantModule(applicant_root)
        applicant_root.mainloop()
    else:
        messagebox.showerror("inicio de sesión exitoso", "Datos incorrectos")

root = tk.Tk()
root.title("Login - IPCArt-Studio")
root.geometry("800x600")

tk.Label(root, text="Nombre de usuario", font=("Helvetica", 30)).pack(pady=20)  # Increase font size and add padding
entry_username = tk.Entry(root, width=90, font=("Helvetica", 10))  # Increase font size
entry_username.pack(ipady=10, pady=10)  # Increase height and add padding

tk.Label(root, text="Contraseña", font=("Helvetica", 30)).pack(pady=20)  # Increase font size and add padding
entry_password = tk.Entry(root, show="*", width=90, font=("Helvetica", 10))  # Increase font size
entry_password.pack(ipady=10, pady=10)  # Increase height and add padding

tk.Button(root, text="INGRESAR", command=login, font=("Helvetica", 20), width=20, height=2).pack(pady=20)  # Increase size and add padding

root.mainloop()

# main.py
import tkinter as tk
from login import login

def main():
    root = tk.Tk()
    login()
    root.mainloop()

if __name__ == "__main__":
    main()