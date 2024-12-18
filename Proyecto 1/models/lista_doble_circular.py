import os

class NodoDobleCircular:
    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.siguiente = None

class ListaDobleCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def __len__(self):
        return self.tamanio
    
    def insertar(self, valor):
        nuevo = NodoDobleCircular(valor)
        # SI ESTA VACIA LA LISTA
        if self.primero == None and self.ultimo == None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo
        # SI LA LISTA NO ESTA VACIA
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo
        self.tamanio += 1

    def generar_grafo(self, id_solicitante):
        if not self.primero:
            return None

        dot = '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
'''
        # CREAMOS LOS NODOS
        actual = self.primero
        contador = 0
        while contador < self.tamanio:
            dot += f'    nodo{contador}[label="{{<f1>|'
            dot += f'ID: {actual.valor["id_figura"]}\\n'
            dot += f'Nombre: {actual.valor["nombre"]}\\n'
            dot += f'Ruta imagen: {actual.valor["ruta_imagen"]}\\n'
            dot += f'|<f2>}}"];\n'
            actual = actual.siguiente
            contador += 1

        # CREAR LOS ENLACES BIDIRECCIONALES
        for i in range(self.tamanio - 1):
            dot += f'    nodo{i}:f2 -> nodo{i+1}:f1[dir=both];\n'

        # ENLACE CIRCULAR ENTRE PRIMERO Y ÚLTIMO
        if self.tamanio > 1:
            dot += f'    nodo0:f1 -> nodo{self.tamanio-1}:f2 [dir=both constraint=false];\n'

        dot += '}'

        # Create directories if they don't exist
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')

        # Save DOT file
        dot_path = f'./reportesdot/Lista_Doble_{id_solicitante}.dot'
        svg_path = f'./Reportes/Lista_Doble_{id_solicitante}.svg'

        with open(dot_path, 'w', encoding='utf-8') as f:
            f.write(dot)

        os.system(f'dot -Tsvg {dot_path} -o {svg_path}')

        return svg_path
