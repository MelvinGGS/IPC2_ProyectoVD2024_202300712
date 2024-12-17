import os

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
        
    def __len__(self):
        return self.tamanio
    
    def insertar(self, valor):
        nuevo = Nodo(valor)
        # SI LA LISTA ESTA VACIA
        if self.primero == None and self.ultimo == None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
        # SI LA LISTA NO ESTA VACIA
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
        self.tamanio += 1

    def generar_grafo(self, id_artista):
        if not self.primero:
            return None
            
        dot = '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
'''
        # CREAMOS LOS NODOS
        contador = 0
        actual = self.primero
        while contador < self.tamanio:
            dot += f'    nodo{contador}[label="{{ID: {actual.valor["id_figura"]}\\n'
            dot += f'Nombre: {actual.valor["nombre"]}\\n'
            dot += f'Solicitante: {actual.valor["solicitante"]}|<f1>}}"];\n'
            actual = actual.siguiente
            contador += 1
            
        # CREAMOS LOS ENLACES
        for i in range(self.tamanio - 1):
            dot += f'    nodo{i} -> nodo{i+1};\n'
            
        # AGREGAMOS EL ULTIMO ENLACE CIRCULAR
        if self.tamanio > 0:
            dot += f'    nodo{self.tamanio-1} -> nodo0[constraint=false];\n'
            
        dot += '}'
        
        # CREAR DIRECTORIOS SI NO EXISTEN
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
            
        # GUARDAR ARCHIVO DOT
        dot_path = f'./reportesdot/Lista_Circular_{id_artista}.dot'
        svg_path = f'./Reportes/Lista_Circular_{id_artista}.svg'
        
        with open(dot_path, 'w', encoding='utf-8') as f:
            f.write(dot)
            
        os.system(f'dot -Tsvg {dot_path} -o {svg_path}')
        
        return svg_path
