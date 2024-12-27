import os
import subprocess

class NodoPila:
    def __init__(self, figura):
        self.figura = figura
        self.abajo = None

class PilaFiguras:
    def __init__(self):
        self.cima = None
        self.tamanio = 0
    
    def push(self, figura):
        nuevo = NodoPila(figura)
        nuevo.abajo = self.cima
        self.cima = nuevo
        self.tamanio += 1
    
    def pop(self):
        if self.cima is None:
            return None
        valor = self.cima.figura
        self.cima = self.cima.abajo
        self.tamanio -= 1
        return valor
    
    def esta_vacia(self):
        return self.cima is None
    
    def generar_grafo(self, id_solicitante):
        if self.esta_vacia():
            return None
            
        # Get absolute path for Reportes directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reportes_dir = os.path.join(base_dir, 'Reportes')
        
        if not os.path.exists(reportes_dir):
            os.makedirs(reportes_dir)
            
        # Generate DOT content with horizontal layout and record shape
        dot = 'digraph G {\n'
        dot += '    rankdir=LR;\n'
        dot += '    node[shape=Mrecord];\n'
        
        # Create single node with all values
        dot += '    Pila[xlabel="Pila" label="'
        
        # Add all values separated by |
        actual = self.cima
<<<<<<< Updated upstream
        valores = []
        while actual:
            valores.append(f"{actual.figura['nombre']}\\n{len(actual.figura['pixels'])} px")
            actual = actual.abajo
        
        dot += '|'.join(valores)
        dot += '"];\n'
=======
        valores_concatenados = ""
        while actual:
            if valores_concatenados:
                valores_concatenados += "|"
            valores_concatenados += f"{actual.figura.nombre}\\n{actual.figura.pixels.tamanio} px"
            actual = actual.abajo
        
        dot += valores_concatenados
        dot += '"]\n'
>>>>>>> Stashed changes
        dot += '}\n'
        
        # Save files
        dot_path = os.path.join(reportes_dir, f'Pila_{id_solicitante}.dot')
        svg_path = os.path.join(reportes_dir, f'Pila_{id_solicitante}.svg')
        
        try:
            with open(dot_path, 'w', encoding='utf-8') as f:
                f.write(dot)
            
            process = subprocess.run(['dot', '-Tsvg', dot_path, '-o', svg_path], 
                                  capture_output=True, 
                                  text=True)
            
            if process.returncode != 0:
                raise Exception(f"Graphviz error: {process.stderr}")
                
            if not os.path.exists(svg_path):
                raise Exception("SVG file was not created")
                
            return svg_path
            
        except Exception as e:
            raise Exception(f"Error generating graph: {str(e)}")
