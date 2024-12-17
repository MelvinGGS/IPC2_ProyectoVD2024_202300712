import os

class NodoDobleCircular:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaDobleCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def insertar(self, valor):
        nuevo = NodoDobleCircular(valor)
        if not self.primero:
            self.primero = nuevo
            self.ultimo = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
        else:
            nuevo.anterior = self.ultimo
            nuevo.siguiente = self.primero
            self.ultimo.siguiente = nuevo
            self.primero.anterior = nuevo
            self.ultimo = nuevo
        self.tamanio += 1
    
    def generar_grafo(self, id_solicitante):
        if not self.primero:
            return None
            
        dot = 'digraph G {\n'
        dot += '    rankdir=LR;\n'
        dot += '    node[shape=record];\n'
        
        # Generar nodos
        actual = self.primero
        contador = 0
        while True:
            imagen = actual.valor
            dot += f'    nodo{contador}[label="'
            dot += f'ID: {imagen["id_figura"]}\\n'
            dot += f'Nombre: {imagen["nombre"]}\\n'
            dot += f'Artista: {imagen["artista"]}'
            dot += '"];\n'
            
            if actual.siguiente != self.primero:
                # Enlaces bidireccionales
                dot += f'    nodo{contador} -> nodo{contador+1};\n'
                dot += f'    nodo{contador+1} -> nodo{contador};\n'
            else:
                # Enlaces circulares bidireccionales
                dot += f'    nodo{contador} -> nodo0;\n'
                dot += f'    nodo0 -> nodo{contador};\n'
                break
            actual = actual.siguiente
            contador += 1
        
        dot += '}'
        
        # Crear directorios si no existen
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
        
        # Guardar archivo DOT
        dot_path = f'./reportesdot/Lista_Doble_{id_solicitante}.dot'
        svg_path = f'./Reportes/Lista_Doble_{id_solicitante}.svg'
        
        with open(dot_path, 'w', encoding='utf-8') as f:
            f.write(dot)
            
        os.system(f'dot -Tsvg {dot_path} -o {svg_path}')
        
        return svg_path
