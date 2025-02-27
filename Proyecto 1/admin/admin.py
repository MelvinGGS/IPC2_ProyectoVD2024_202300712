import sys
import os
import re  # Add this import at the top
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as ET
from models.linked_list import ListaDoblementeEnlazada
from models.simple_list import ListaSimple
from PIL import Image, ImageTk

class ModuloAdmin:
    def __init__(self, root):
        self.root = root
        self.root.title("ADMINISTRADOR")
        root.geometry("1400x725")
        self.solicitantes = ListaDoblementeEnlazada()
        self.artistas = ListaSimple()
        self.etiqueta_imagen = tk.Label(root)  # Initialize here instead of None
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="Módulo administrador", font=("Helvetica", 16)).pack(pady=2)
        
        marco_botones = tk.Frame(self.root)
        marco_botones.pack(pady=1)
        
        tk.Button(marco_botones, text="Cargar Solicitantes", command=self.cargar_solicitantes, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Ver Solicitantes", command=self.ver_solicitantes, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Cargar Artistas", command=self.cargar_artistas, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Ver Artistas", command=self.ver_artistas, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Cerrar Sesión", command=self.cerrar_sesion, 
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)

        # Marco para mostrar imágenes
        self.marco_imagen = tk.Frame(self.root)
        self.marco_imagen.pack(pady=2, fill=tk.BOTH, expand=True)
        
        # Barra de desplazamiento horizontal
        barra_h = tk.Scrollbar(self.marco_imagen, orient=tk.HORIZONTAL)
        barra_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        altura_max_canvas = 645
        
        self.canvas = tk.Canvas(self.marco_imagen, height=altura_max_canvas, xscrollcommand=barra_h.set)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        barra_h.config(command=self.canvas.xview)
        
        # Initialize and pack the image label properly
        self.etiqueta_imagen = tk.Label(self.canvas)
        self.canvas.create_window((0, 0), window=self.etiqueta_imagen, anchor='nw')

    def cargar_solicitantes(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta_archivo:
            try:
                self.cargar_solicitantes_xml(ruta_archivo)
                messagebox.showinfo("Éxito", "Archivo XML cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

    def cargar_artistas(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta_archivo:
            try:
                self.cargar_artistas_xml(ruta_archivo)
                messagebox.showinfo("Éxito", "Archivo de artistas XML cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

    def cargar_solicitantes_xml(self, ruta_archivo):
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
<<<<<<< Updated upstream
=======
        duplicados = set()  # Replaced list with a set
>>>>>>> Stashed changes

        for solicitante in root.findall('solicitante'):
            id = solicitante.get('id')
            
            # Validar formato ID
            if not id.startswith('IPC-'):
<<<<<<< Updated upstream
                raise ValueError(f"ID inválido: {id}. Debe comenzar con 'IPC-'")

            # Validar ID único
            if self.solicitantes.buscar_por_id(id):
                raise ValueError(f"ID duplicado: {id}")
=======
                messagebox.showwarning("Advertencia", f"ID inválido omitido: {id}. Debe comenzar con 'IPC-'")
                continue

            # Verificar duplicados
            if self.solicitantes.buscar_por_id(id):
                duplicados.add(id)  # Using set to store duplicates
                continue
>>>>>>> Stashed changes

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
            self.solicitantes.agregar(datos_solicitante)

<<<<<<< Updated upstream
    def cargar_artistas_xml(self, ruta_archivo):
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
=======
        if duplicados:
            messagebox.showinfo("Información", f"Se omitieron los siguientes IDs duplicados: {', '.join(duplicados)}")

    def cargar_artistas_xml(self, ruta_archivo):
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
        duplicados = set()  # Replaced list with a set
>>>>>>> Stashed changes

        for artista in root.findall('Artista'):
            id = artista.get('id')
            
            # Validar formato ID
            if not id.startswith('ART-'):
<<<<<<< Updated upstream
                raise ValueError(f"ID inválido: {id}. Debe comenzar con 'ART-'")

            # Validar ID único
            if self.artistas.buscar_por_id(id):
                raise ValueError(f"ID duplicado: {id}")
=======
                messagebox.showwarning("Advertencia", f"ID inválido omitido: {id}. Debe comenzar con 'ART-'")
                continue

            # Verificar duplicados
            if self.artistas.buscar_por_id(id):
                duplicados.add(id)  # Using set to store duplicates
                continue
>>>>>>> Stashed changes

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
            self.artistas.agregar(datos_artista)

<<<<<<< Updated upstream
=======
        if duplicados:
            messagebox.showinfo("Información", f"Se omitieron los siguientes IDs duplicados: {', '.join(duplicados)}")

>>>>>>> Stashed changes
    def ver_solicitantes(self):
        if not self.solicitantes.primero:  # Changed from head to primero
            messagebox.showinfo("Info", "No hay solicitantes cargados")
            return
            
        try:
            ruta_imagen = self.solicitantes.generar_grafo()
            self.mostrar_imagen_svg(ruta_imagen)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el grafo: {str(e)}")

    def ver_artistas(self):
        if not self.artistas.primero:  # Changed from head to primero
            messagebox.showinfo("Info", "No hay artistas cargados")
            return
            
        try:
            ruta_imagen = self.artistas.generar_grafo()
            self.mostrar_imagen_svg(ruta_imagen)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el grafo: {str(e)}")

    def cerrar_sesion(self):
        ventana_login = tk.Tk()
        from login import LoginWindow
        app = LoginWindow(ventana_login, self.artistas, self.solicitantes)  # Pasamos las listas como parámetros
        self.root.destroy()
        ventana_login.mainloop()

    def mostrar_imagen_svg(self, image_path):
        try:
            # First check if directories exist
            if not os.path.exists('./Reportes'):
                os.makedirs('./Reportes')
            if not os.path.exists('./reportesdot'):
                os.makedirs('./reportesdot')

            from cairosvg import svg2png
            png_path = image_path.replace('.svg', '.png')
            svg2png(url=image_path, write_to=png_path)
            
            # Load image
            image = Image.open(png_path)
            
            # Usar casi toda la altura disponible de la ventana
            max_height = 450
            
            # Calculate new dimensions maintaining aspect ratio
            aspect_ratio = image.width / image.height
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update image label
            if self.etiqueta_imagen:
                self.etiqueta_imagen.configure(image=photo)
                self.etiqueta_imagen.image = photo  # Keep a reference!
                
                # Update canvas scrollregion
                self.canvas.configure(scrollregion=(0, 0, new_width, new_height))
            else:
                raise Exception("Image label not initialized")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la imagen: {str(e)}")
