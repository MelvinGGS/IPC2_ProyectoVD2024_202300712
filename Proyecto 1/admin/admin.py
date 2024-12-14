# admin_module.py
import tkinter as tk
<<<<<<< Updated upstream
from tkinter import messagebox
=======
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as ET
import re
from models.linked_list import DoublyLinkedList
from models.simple_list import SimpleList
from PIL import Image, ImageTk  # Add this import
>>>>>>> Stashed changes

class AdminModule:
    def __init__(self, root):
        self.root = root
        self.root.title("ADMINISTRADOR")
<<<<<<< Updated upstream
        root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Modulo administrador", font=("Helvetica", 16)).pack(pady=20)  # Increase font size and add padding
        tk.Button(self.root, text="Usuarios", command=self.manage_users, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding
        tk.Button(self.root, text="Contenido", command=self.manage_content, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding
        tk.Button(self.root, text="Salir", command=self.logout, font=("Helvetica", 16), width=20, height=2).pack(pady=10)  # Increase size and add padding

    def manage_users(self):
        # ...existing code...
        messagebox.showinfo("Manage Users", "User management functionality")

    def manage_content(self):
        # ...existing code...
        messagebox.showinfo("Manage Content", "Content management functionality")
=======
        root.geometry("1400x725")
        self.solicitantes = DoublyLinkedList()
        self.artistas = SimpleList()
        self.image_label = None
        self.crear_widgets()

    def crear_widgets(self):
        # Minimizar al máximo los paddings
        tk.Label(self.root, text="Modulo administrador", font=("Helvetica", 16)).pack(pady=2)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=1)
        
        # Create buttons in the frame
        tk.Button(button_frame, text="Cargar Solicitantes", command=self.manejar_solicitantes, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Ver Solicitantes", command=self.ver_solicitantes, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cargar Artistas", command=self.manejar_artistas, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Ver Artistas", command=self.ver_artistas, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cerrar Sesión", command=self.logout, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)

        # Create main frame for image display with scrollbar
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=2, fill=tk.BOTH, expand=True)
        
        # Add horizontal scrollbar
        h_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Maximizar altura del canvas (ventana 725px - espacio para título/botones/scrollbar ≈ 80px)
        max_canvas_height = 645  
        
        # Add canvas with scrollbar and fixed height
        self.canvas = tk.Canvas(self.image_frame, height=max_canvas_height, xscrollcommand=h_scrollbar.set)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        h_scrollbar.config(command=self.canvas.xview)
        
        # Create label inside canvas
        self.image_label = tk.Label(self.canvas, text="Área de imagen")
        self.canvas.create_window((0, 0), window=self.image_label, anchor='nw')

    def manejar_solicitantes(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            try:
                self.cargar_solicitantes_xml(file_path)
                messagebox.showinfo("Éxito", "Archivo XML cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

    def manejar_artistas(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            try:
                self.cargar_artistas_xml(file_path)
                messagebox.showinfo("Éxito", "Archivo de artistas XML cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")


    def cargar_solicitantes_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for solicitante in root.findall('solicitante'):
            id = solicitante.get('id')
            
            # Validar formato ID
            if not id.startswith('IPC-'):
                raise ValueError(f"ID inválido: {id}. Debe comenzar con 'IPC-'")
            
            # Validar ID único
            if self.solicitantes.search_by_id(id):
                raise ValueError(f"ID duplicado: {id}")

            # Extraer datos
            datos_solicitante = {
                'id': id,
                'pwd': solicitante.get('pwd'),
                'nombre': solicitante.find('NombreCompleto').text,
                'correo': solicitante.find('CorreoElectronico').text,
                'telefono': solicitante.find('NumeroTelefono').text,
                'direccion': solicitante.find('Direccion').text
            }

            # Agregar a la lista
            self.solicitantes.append(datos_solicitante)

    def cargar_artistas_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for artista in root.findall('Artista'):
            id = artista.get('id')
            
            # Validar formato ID
            if not id.startswith('ART-'):
                raise ValueError(f"ID inválido: {id}. Debe comenzar con 'ART-'")
            
            # Validar ID único
            if self.artistas.search_by_id(id):
                raise ValueError(f"ID duplicado: {id}")

            # Extraer datos
            datos_artista = {
                'id': id,
                'pwd': artista.get('pwd'),
                'nombre': artista.find('NombreCompleto').text,
                'correo': artista.find('CorreoElectronico').text,
                'telefono': artista.find('NumeroTelefono').text,
                'especialidades': artista.find('Especialidades').text,
                'notas': artista.find('NotasAdicionales').text
            }

            # Agregar a la lista
            self.artistas.append(datos_artista)

    def ver_solicitantes(self):
        if not self.solicitantes.primero:  # Changed from head to primero
            messagebox.showinfo("Info", "No hay solicitantes cargados")
            return
            
        try:
            image_path = self.solicitantes.generate_graph()
            self.mostrar_imagen_svg(image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el grafo: {str(e)}")

    def ver_artistas(self):
        if not self.artistas.primero:  # Changed from head to primero
            messagebox.showinfo("Info", "No hay artistas cargados")
            return
            
        try:
            image_path = self.artistas.generate_graph()
            self.mostrar_imagen_svg(image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el grafo: {str(e)}")
>>>>>>> Stashed changes

    def logout(self):
        # ...existing code...
        self.root.destroy()
<<<<<<< Updated upstream
        # main function is not defined, so we remove the call
=======
        # main function is not defined, so we remove the call

    def mostrar_imagen_svg(self, image_path):
        try:
            from cairosvg import svg2png
            png_path = image_path.replace('.svg', '.png')
            svg2png(url=image_path, write_to=png_path)
            
            # Load image
            image = Image.open(png_path)
            
            # Usar casi toda la altura disponible de la ventana
            max_height = 500  # Dejamos 10px de margen
            
            # Calculate new dimensions maintaining aspect ratio
            aspect_ratio = image.width / image.height
            new_height = max_height  # Forzamos usar altura máxima
            new_width = int(new_height * aspect_ratio)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update image label
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            
            # Update canvas scrollregion
            self.canvas.configure(scrollregion=(0, 0, new_width, new_height))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la imagen: {str(e)}))")

    def display_image(self, image_path):
        try:
            # Load and resize image
            image = Image.open(image_path)
            image = image.resize((900, 550), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update image label
            if self.image_label:
                self.image_label.configure(image=photo)
                self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)})")
>>>>>>> Stashed changes
