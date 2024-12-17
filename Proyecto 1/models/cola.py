import os

class NodoCola:  # Make sure this is above Cola class since it's used by Cola
    def __init__(self, figura, solicitante_id):
        self.figura = figura
        self.solicitante_id = solicitante_id
        self.siguiente = None

class Cola:  # Changed from 'cola' to 'Cola'
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def esta_vacia(self):
        return self.primero is None
    
    def encolar(self, figura, solicitante_id):
        nuevo = NodoCola(figura, solicitante_id)
        if self.esta_vacia():
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.tamanio += 1
    
    def desencolar(self):
        if self.esta_vacia():
            return None
        figura = self.primero.figura
        solicitante_id = self.primero.solicitante_id
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        self.tamanio -= 1
        return figura, solicitante_id
    
    def generar_grafo(self):
        if self.esta_vacia():
            return None
            
        dot = 'digraph G {\n'
        dot += '    rankdir=LR;\n'
        dot += '    node[shape=record];\n'
        
        actual = self.primero
        contador = 0
        while actual:
            dot += f'    nodo{contador}[label="{{ID: {actual.figura["id"]}\\n'
            dot += f'Nombre: {actual.figura["nombre"]}\\n'
            dot += f'Solicitante: {actual.solicitante_id}}}"];\n'
            if contador > 0:
                dot += f'    nodo{contador-1} -> nodo{contador};\n'
            actual = actual.siguiente
            contador += 1
        
        dot += '}'
        
        # Create directories if they don't exist
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
        
        # Save DOT file
        dot_path = './reportesdot/Cola.dot'
        with open(dot_path, 'w', encoding='utf-8') as f:
            f.write(dot)
        
        # Generate image
        img_path = './Reportes/Cola.svg'
        os.system(f'dot -Tsvg {dot_path} -o {img_path}')
        
        return img_path
