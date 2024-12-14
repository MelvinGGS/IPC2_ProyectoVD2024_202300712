import os

class Node:
    def __init__(self, data):
        self.valor = data
        self.anterior = None
        self.siguiente = None

class DoublyLinkedList:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def __len__(self):
        return self.tamanio

    def append(self, data):
        nuevo = Node(data)
        if self.primero is None and self.ultimo is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamanio += 1

    def search_by_id(self, id):
        actual = self.primero
        while actual:
            if actual.valor.get('id') == id:
                return True
            actual = actual.siguiente
        return False

    def generate_graph(self):
        codigo_dot = '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
'''
        # Crear nodos
        actual = self.primero
        contador = 1
        while actual:
            node_content = f'{actual.valor["id"]}\\nNombre: {actual.valor["nombre"]}\\nCorreo: {actual.valor["correo"]}'
            codigo_dot += f'    nodo{contador}[label=\"{{<f1>|{node_content}|<f2>}}\"];\n'
            contador += 1
            actual = actual.siguiente
        
        # Crear enlaces bidireccionales
        actual = self.primero
        contador = 1
        while actual and actual.siguiente:
            # Enlace hacia adelante
            codigo_dot += f'    nodo{contador}:f2 -> nodo{contador+1}:f1;\n'
            # Enlace hacia atrás
            codigo_dot += f'    nodo{contador+1}:f1 -> nodo{contador}:f2;\n'
            contador += 1
            actual = actual.siguiente
        
        codigo_dot += '}'
        
        # Crear directorios si no existen
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
        
        # Guardar archivo DOT
        dot_path = './reportesdot/ListaSolicitantes.dot'
        with open(dot_path, 'w') as f:
            f.write(codigo_dot)
        
        # Generar imagen
        img_path = './Reportes/ListaSolicitantes.svg'
        os.system(f'dot -Tsvg {dot_path} -o {img_path}')
        
        return img_path
