import tkinter as tk
from login import LoginWindow

def principal():
    ventana = tk.Tk()
    app = LoginWindow(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    principal()