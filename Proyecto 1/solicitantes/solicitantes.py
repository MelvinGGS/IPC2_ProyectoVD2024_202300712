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
    def __init__(self, root, lista_artistas=None, lista_solicitantes=None, pila_figuras=None):
        self.root = root
        self.root.title("SOLICITANTES")
        root.geometry("1400x725")
        self.lista_artistas = lista_artistas
        self.lista_solicitantes = lista_solicitantes
        # Store state
        if not hasattr(ModuloSolicitantes, '_pila_global'):
            ModuloSolicitantes._pila_global = PilaFiguras()
        
        self.pila_figuras = ModuloSolicitantes._pila_global
        if pila_figuras and pila_figuras.tamanio > 0:
            temp_stack = PilaFiguras()
            while not pila_figuras.esta_vacia():
                temp_stack.push(pila_figuras.pop())
            while not temp_stack.esta_vacia():
                self.pila_figuras.push(temp_stack.pop())
        self.id_solicitante = None
        self.etiqueta_imagen = None
        self.lista_imagenes = ListaDobleCircular()
        self.indice_imagen_actual = 0
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

        # Create main container frame
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(expand=True, fill=tk.BOTH)
        
        # Crear frame para la imagen
        self.frame_imagen = tk.Frame(self.frame_principal)
        self.frame_imagen.pack(expand=True, fill=tk.BOTH, pady=5)
        
        # Barra de desplazamiento horizontal
        barra_h = tk.Scrollbar(self.frame_imagen, orient=tk.HORIZONTAL)
        barra_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas configuration
        self.canvas = tk.Canvas(self.frame_imagen, height=500, xscrollcommand=barra_h.set)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        barra_h.config(command=self.canvas.xview)
        
        # Frame contenedor para la imagen
        self.frame_contenido = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor='nw')
        
        # Etiqueta para la imagen
        self.etiqueta_imagen = tk.Label(self.frame_contenido)
        self.etiqueta_imagen.pack(expand=True, fill=tk.BOTH)
        
        # Frame para botones de navegación
        self.frame_navegacion = tk.Frame(self.frame_principal)
        self.frame_navegacion.pack(side=tk.BOTTOM, pady=10)
        
        # Botones de navegación
        self.btn_anterior = tk.Button(self.frame_navegacion, text="Anterior", 
                                    command=self.imagen_anterior,
                                    state=tk.DISABLED)
        self.btn_anterior.pack(side=tk.LEFT, padx=5)
        
        self.btn_siguiente = tk.Button(self.frame_navegacion, text="Siguiente", 
                                     command=self.imagen_siguiente,
                                     state=tk.DISABLED)
        self.btn_siguiente.pack(side=tk.LEFT, padx=5)

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
            
            # Simplemente apilar la figura sin más procesamiento
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
            
            image = Image.open(png_path)
            
            # Calculate dimensions to fit in window
            window_width = self.frame_imagen.winfo_width() or 800
            window_height = self.frame_imagen.winfo_height() or 500
            
            # Calculate scaling
            img_ratio = image.width / image.height
            window_ratio = window_width / window_height
            
            if img_ratio > window_ratio:
                new_width = window_width
                new_height = int(window_width / img_ratio)
            else:
                new_height = window_height
                new_width = int(window_height * img_ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            self.etiqueta_imagen.configure(image=photo)
            self.etiqueta_imagen.image = photo
            
            # Update canvas scrollregion
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
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
            imagenes = []
            
            while actual:
                if actual.valor['id'] == self.id_solicitante:
                    if 'imagenes' in actual.valor:
                        imagenes = actual.valor['imagenes']
                    break
                actual = actual.siguiente
                
            if not imagenes:
                messagebox.showinfo("Info", "No hay imágenes procesadas")
                return

            # Clear existing images and add new ones
            self.lista_imagenes = ListaDobleCircular()
            for imagen in imagenes:
                self.lista_imagenes.insertar(imagen)
            
            self.indice_imagen_actual = 0
            self.mostrar_imagen_actual()
            self.actualizar_estados_botones()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar las imágenes: {str(e)}")

    def imagen_anterior(self):
        if self.indice_imagen_actual > 0:
            self.indice_imagen_actual -= 1
            self.mostrar_imagen_actual()
        self.actualizar_estados_botones()

    def imagen_siguiente(self):
        if self.indice_imagen_actual < len(self.lista_imagenes) - 1:
            self.indice_imagen_actual += 1
            self.mostrar_imagen_actual()
        self.actualizar_estados_botones()

    def actualizar_estados_botones(self):
        self.btn_anterior['state'] = tk.NORMAL if self.indice_imagen_actual > 0 else tk.DISABLED
        self.btn_siguiente['state'] = tk.NORMAL if self.indice_imagen_actual < len(self.lista_imagenes) - 1 else tk.DISABLED

    def mostrar_imagen_actual(self):
        if self.lista_imagenes.tamanio == 0:
            return
            
        # Get current image
        actual = self.lista_imagenes.primero
        for _ in range(self.indice_imagen_actual):
            actual = actual.siguiente
            if actual == self.lista_imagenes.primero:
                break
                
        if actual and 'ruta_imagen' in actual.valor:
            self.mostrar_imagen_svg(actual.valor['ruta_imagen'])

    def cerrar_sesion(self):
        ventana_login = tk.Tk()
        from login import LoginWindow
        # Pass the current pile state
        app = LoginWindow(ventana_login, self.lista_artistas, 
                         self.lista_solicitantes, self.pila_figuras)
        self.root.destroy()
        ventana_login.mainloop()