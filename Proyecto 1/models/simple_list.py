import os

class Nodo:
    def __init__(self, datos):
        self.valor = datos
        self.siguiente = None

class ListaSimple:
    def __init__(self):
        self.primero = None
        self.tamanio = 0
    
    def __len__(self):
        return self.tamanio
    
    def agregar(self, datos):
        # Validar si ya existe
        if self.buscar_por_id(datos['id']):
            return False
            
        nuevo = Nodo(datos)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1
        return True

    def buscar_por_id(self, id):
        actual = self.primero
        while actual:
            if actual.valor.get('id') == id:
                return True
            actual = actual.siguiente
        return False

    def generar_grafo(self):
        # Crear el contenido del archivo DOT
        contenido_dot = '''digraph G {
    charset="utf-8"
    rankdir=LR;
    node[shape=record, height=.1]\n'''
        
        # Generar nodos con codificación utf-8
        actual = self.primero
        contador = 1
        while actual:
            contenido_nodo = f'{actual.valor["id"]}\\nNombre: {actual.valor["nombre"]}\\nCorreo: {actual.valor["correo"]}'
            contenido_dot += f'    nodo{contador}[label="{contenido_nodo}"];\n'
            contador += 1
            actual = actual.siguiente
        
        # Generar enlaces
        actual = self.primero
        contador = 1
        while actual.siguiente:
            contenido_dot += f'    nodo{contador} -> nodo{str(contador+1)};\n'
            contador += 1
            actual = actual.siguiente
        
        contenido_dot += '}'
        
        # Crear directorios si no existen
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
            
        # Guardar archivo DOT con codificación utf-8
        ruta_dot = './reportesdot/ListaArtistas.dot'
        with open(ruta_dot, 'w', encoding='utf-8') as f:
            f.write(contenido_dot)
            
        # Generar imagen especificando la codificación
        ruta_img = './Reportes/ListaArtistas.svg'
        os.system(f'dot -Tsvg {ruta_dot} -o {ruta_img} -Gcharset=utf8')
        
        return ruta_img