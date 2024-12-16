import tkinter as tk
from login import iniciar_sesion

def principal():
    ventana = tk.Tk()
    iniciar_sesion()
    ventana.mainloop() 

if __name__ == "__main__":
    principal()