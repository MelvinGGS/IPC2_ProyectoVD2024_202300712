# artist_module.py
import tkinter as tk
from tkinter import messagebox
from models.cola import Cola  # Changed import
from models.stack import PilaFiguras
from models.matriz_dispersa import MatrizDispersa
from PIL import Image, ImageTk
from models.lista_circular import ListaCircular

class ModuloArtista:
    # Add class-level shared queue
    _cola_global = Cola()

    def __init__(self, root, lista_artistas=None, lista_solicitantes=None):
        self.root = root
        self.root.title("ARTISTAS")
        root.geometry("1400x725")
        self.lista_artistas = lista_artistas
        self.lista_solicitantes = lista_solicitantes
        self.id_artista = None
        self.etiqueta_imagen = None
        self.lista_imagenes = ListaCircular()
        self.crear_widgets()
        if not hasattr(ModuloArtista, '_cola_global'):
            ModuloArtista._cola_global = Cola()

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
        tk.Button(marco_botones, text="Imágenes procesadas", command=self.modificar_perfil,
                 font=("Helvetica", 12), width=20, height=2).pack(side=tk.LEFT, padx=10)
        tk.Button(marco_botones, text="Cerrar Sesión", command=self.cerrar_sesion,
                 font=("Helvetica", 12), width=15, height=2).pack(side=tk.LEFT, padx=10)

        # Marco para mostrar imágenes
        self.marco_imagen = tk.Frame(self.root)
        self.marco_imagen.pack(pady=2, fill=tk.BOTH, expand=True)
        
        # Barra de desplazamiento horizontal
        barra_h = tk.Scrollbar(self.marco_imagen, orient=tk.HORIZONTAL)
        barra_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas = tk.Canvas(self.marco_imagen, height=645, xscrollcommand=barra_h.set)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        barra_h.config(command=self.canvas.xview)
        
        # Restore original image positioning
        self.etiqueta_imagen = tk.Label(self.canvas)
        self.canvas.create_window((0, 0), window=self.etiqueta_imagen, anchor='nw')

    def ver_solicitudes(self):
        if not self.id_artista:
            messagebox.showerror("Error", "ID de artista no establecido")
            return
            
        # Buscar el artista actual
        artista = None
        actual = self.lista_artistas.primero
        while actual:
            if actual.valor['id'] == self.id_artista:
                artista = actual.valor
                break
            actual = actual.siguiente
            
        if not artista:
            messagebox.showerror("Error", "Artista no encontrado")
            return
            
        # Use global queue instead of individual artist queue
        if ModuloArtista._cola_global.esta_vacia():
            messagebox.showinfo("Info", "No hay solicitudes pendientes")
            return
            
        # Process the request from global queue
        figura, solicitante_id = ModuloArtista._cola_global.desencolar()
        
        # Crear y procesar matriz dispersa
        matriz = MatrizDispersa()
        for pixel in figura['pixels']:
            matriz.insertar(pixel['fila'], pixel['col'], pixel['color'])
            
        # Generar imagen
        ruta_imagen = matriz.graficar(figura['id'])
        
        # Guardar la imagen procesada en el artista
        imagen_procesada = {
            'id_figura': figura['id'],
            'nombre': figura['nombre'],
            'solicitante': solicitante_id,
            'ruta_imagen': ruta_imagen
        }
        if 'imagenes_procesadas' not in artista:
            artista['imagenes_procesadas'] = []
        artista['imagenes_procesadas'].append(imagen_procesada)
        
        # También guardar en la lista circular para visualización
        self.lista_imagenes.insertar(imagen_procesada)
        
        # Actualizar solicitante
        solicitante = None
        actual = self.lista_solicitantes.primero
        while actual:
            if actual.valor['id'] == solicitante_id:
                if 'imagenes' not in actual.valor:
                    actual.valor['imagenes'] = []
                actual.valor['imagenes'].append({
                    'id_figura': figura['id'],
                    'nombre': figura['nombre'],
                    'artista': self.id_artista,
                    'ruta_imagen': ruta_imagen
                })
                break
            actual = actual.siguiente
            
        messagebox.showinfo("Éxito", "Solicitud procesada correctamente")
        self.mostrar_imagen_svg(ruta_imagen)

    def ver_perfil(self):
        if not self.id_artista:
            messagebox.showerror("Error", "ID de artista no establecido")
            return
            
        try:
            # Use global queue for visualization
            ruta_imagen = ModuloArtista._cola_global.generar_grafo()
            if ruta_imagen:
                self.mostrar_imagen_svg(ruta_imagen)
            else:
                messagebox.showinfo("Info", "No hay solicitudes en cola")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar cola: {str(e)}")

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

    def modificar_perfil(self):
        if not self.id_artista:
            messagebox.showerror("Error", "ID de artista no establecido")
            return
            
        try:
            ruta_imagen = self.lista_imagenes.generar_grafo(self.id_artista)
            if ruta_imagen:
                self.mostrar_imagen_svg(ruta_imagen)
            else:
                messagebox.showinfo("Info", "No hay imágenes procesadas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar visualización: {str(e)}")

    def cerrar_sesion(self):
        ventana_login = tk.Tk()
        from login import LoginWindow
        app = LoginWindow(ventana_login, self.lista_artistas, self.lista_solicitantes)
        self.root.destroy()
        ventana_login.mainloop()