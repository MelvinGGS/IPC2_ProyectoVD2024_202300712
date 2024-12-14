import os

class Node:
    def __init__(self, data):
        self.valor = data
        self.siguiente = None

class SimpleList:
    def __init__(self):
        self.primero = None
        self.tamanio = 0
    
    def __len__(self):
        return self.tamanio
    
    def append(self, data):
        # Validar si ya existe
        if self.search_by_id(data['id']):
            return False
            
        nuevo = Node(data)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1
        return True

    def search_by_id(self, id):
        actual = self.primero
        while actual:
            if actual.valor.get('id') == id:
                return True
            actual = actual.siguiente
        return False

    def generate_graph(self):
        # Crear el contenido del archivo DOT
        dot_content = '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]\n'''
        
        # Generar nodos
        actual = self.primero
        contador = 1
        while actual:
            node_content = f'{actual.valor["id"]}\\nNombre: {actual.valor["nombre"]}\\nCorreo: {actual.valor["correo"]}'
            dot_content += f'    nodo{contador}[label="{node_content}"];\n'
            contador += 1
            actual = actual.siguiente
        
        # Generar enlaces
        actual = self.primero
        contador = 1
        while actual.siguiente:
            dot_content += f'    nodo{contador} -> nodo{str(contador+1)};\n'
            contador += 1
            actual = actual.siguiente
        
        dot_content += '}'
        
        # Crear directorios si no existen
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
            
        # Guardar archivo DOT
        dot_path = './reportesdot/ListaArtistas.dot'
        with open(dot_path, 'w') as f:
            f.write(dot_content)
            
        # Generar imagen
        img_path = './Reportes/ListaArtistas.svg'
        os.system(f'dot -Tsvg {dot_path} -o {img_path}')
        
        return img_path
