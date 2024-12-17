# modulo_solicitantes.py
import tkinter as tk
from tkinter import messagebox, filedialog
import xml.etree.ElementTree as ET
from models.cola import Cola  # Changed import
from models.stack import PilaFiguras
import os
from PIL import Image, ImageTk
from models.lista_doble_circular import ListaDobleCircular

class ModuloSolicitantes:
    def __init__(self, root, lista_artistas=None, lista_solicitantes=None):
        self.root = root
        self.root.title("SOLICITANTES")
        root.geometry("1400x725")
        # Guardar referencia a las listas
        self.lista_artistas = lista_artistas
        self.lista_solicitantes = lista_solicitantes
        self.pila_figuras = PilaFiguras()
        self.id_solicitante = None  # Se debe establecer al iniciar sesión
        self.etiqueta_imagen = None
        self.lista_imagenes = ListaDobleCircular()
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
        
        self.etiqueta_imagen = tk.Label(self.canvas)
        self.canvas.create_window((0, 0), window=self.etiqueta_imagen, anchor='nw')

    def ver_artistas(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if not ruta_archivo:
            return
            
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            figura = {
                'id': root.find('nombre').get('id'),
                'nombre': root.find('nombre').text,
                'pixels': []
            }
            
            for pixel in root.find('diseño').findall('pixel'):
                figura['pixels'].append({
                    'fila': int(pixel.get('fila')),
                    'col': int(pixel.get('col')),
                    'color': pixel.text
                })
            
            self.pila_figuras.push(figura)
            messagebox.showinfo("Éxito", "Figura cargada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la figura: {str(e)}")

    def aplicar_proyecto(self):
        if self.pila_figuras.esta_vacia():
            messagebox.showinfo("Info", "No hay figuras en la pila para solicitar")
            return
        
        try:
            figura = self.pila_figuras.pop()
            
            if not self.lista_artistas or self.lista_artistas.primero is None:
                messagebox.showerror("Error", "No hay artistas disponibles")
                self.pila_figuras.push(figura)  # Devolver la figura a la pila
                return
                
            artista = self.lista_artistas.primero.valor
            # Cambiar la forma de inicializar la cola
            if 'cola_solicitudes' not in artista:
                artista['cola_solicitudes'] = Cola()
            
            artista['cola_solicitudes'].encolar(figura, self.id_solicitante)
            messagebox.showinfo("Éxito", "Solicitud enviada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar la solicitud: {str(e)}")

    def ver_aplicaciones(self):
        if self.pila_figuras.esta_vacia():
            messagebox.showinfo("Info", "No hay figuras en la pila")
            return
            
        try:
            ruta_imagen = self.pila_figuras.generar_grafo(self.id_solicitante)
            if ruta_imagen and os.path.exists(ruta_imagen):
                self.mostrar_imagen_svg(ruta_imagen)
            else:
                raise Exception(f"No se pudo encontrar el archivo: {ruta_imagen}")
        except Exception as e:
            messagebox.showerror("Error", 
                f"Error al generar el grafo: {str(e)}\n\n"
                "Asegúrese de que Graphviz esté instalado correctamente en el sistema.")

    def mostrar_imagen_svg(self, image_path):
        try:
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
            self.etiqueta_imagen.configure(image=photo)
            self.etiqueta_imagen.image = photo
            
            # Update canvas scrollregion
            self.canvas.configure(scrollregion=(0, 0, new_width, new_height))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la imagen: {str(e)}")

    def ver_perfil(self):
        try:
            # Buscar el solicitante actual
            actual = self.lista_solicitantes.primero
            while actual:
                if actual.valor['id'] == self.id_solicitante:
                    if 'imagenes' in actual.valor:
                        for imagen in actual.valor['imagenes']:
                            self.lista_imagenes.insertar(imagen)
                    break
                actual = actual.siguiente
            
            if self.lista_imagenes.tamanio == 0:
                messagebox.showinfo("Info", "No hay imágenes procesadas")
                return
                
            ruta_imagen = self.lista_imagenes.generar_grafo(self.id_solicitante)
            if ruta_imagen:
                self.mostrar_imagen_svg(ruta_imagen)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la lista de imágenes: {str(e)}")

    def modificar_perfil(self):
        try:
            actual = self.lista_solicitantes.primero
            imagenes_mostradas = []
            
            while actual:
                if actual.valor['id'] == self.id_solicitante:
                    if 'imagenes' in actual.valor:
                        for imagen in actual.valor['imagenes']:
                            if imagen['ruta_imagen'] not in imagenes_mostradas:
                                self.mostrar_imagen_svg(imagen['ruta_imagen'])
                                imagenes_mostradas.append(imagen['ruta_imagen'])
                    break
                actual = actual.siguiente
                
            if not imagenes_mostradas:
                messagebox.showinfo("Info", "No hay imágenes para mostrar")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar las imágenes: {str(e)}")

    def cerrar_sesion(self):
        ventana_login = tk.Tk()
        from login import LoginWindow
        app = LoginWindow(ventana_login, self.lista_artistas, self.lista_solicitantes)
        self.root.destroy()
        ventana_login.mainloop()