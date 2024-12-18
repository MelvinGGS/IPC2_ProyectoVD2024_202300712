import os

class NodoCabecera:
    def __init__(self, id):
        self.id = id
        self.siguiente = None
        self.anterior = None
        self.acceso = None

class NodoCelda:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y 
        self.valor = valor
        self.arriba = None
        self.abajo = None
        self.izquierda = None
        self.derecha = None

class ListaCabecera:
    def __init__(self, coordenada):
        self.coordenada = coordenada
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def insertarNodoCabecera(self, nuevo):
        if self.primero == None and self.ultimo == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            if nuevo.id < self.primero.id:
                nuevo.siguiente = self.primero
                self.primero.anterior = nuevo
                self.primero = nuevo
            elif nuevo.id > self.ultimo.id:
                self.ultimo.siguiente = nuevo
                nuevo.anterior = self.ultimo
                self.ultimo = nuevo
            else:
                actual = self.primero
                while actual != None:
                    if nuevo.id < actual.id:
                        nuevo.siguiente = actual
                        nuevo.anterior = actual.anterior
                        actual.anterior.siguiente = nuevo
                        actual.anterior = nuevo
                        break
                    elif nuevo.id > actual.id:
                        actual = actual.siguiente
                    else:
                        break
        self.tamanio += 1
    
    def obtenerCabecera(self, id):
        actual = self.primero
        while actual != None:
            if actual.id == id:
                return actual
            actual = actual.siguiente
        return None

class MatrizDispersa:
    def __init__(self):
        self.filas = ListaCabecera('fila')
        self.columnas = ListaCabecera('columna')

    def insertar(self, x, y, valor):
        nuevo = NodoCelda(x, y, valor)
        
        # Buscar o crear cabeceras
        celda_x = self.filas.obtenerCabecera(x)
        celda_y = self.columnas.obtenerCabecera(y)

        if celda_x == None:
            celda_x = NodoCabecera(x)
            self.filas.insertarNodoCabecera(celda_x)

        if celda_y == None:
            celda_y = NodoCabecera(y)
            self.columnas.insertarNodoCabecera(celda_y)

        # Insertar en fila
        if celda_x.acceso == None:
            celda_x.acceso = nuevo
        else:
            if nuevo.y < celda_x.acceso.y:
                nuevo.derecha = celda_x.acceso
                celda_x.acceso.izquierda = nuevo
                celda_x.acceso = nuevo
            else:
                actual = celda_x.acceso
                while actual != None:
                    if nuevo.y < actual.y:
                        nuevo.derecha = actual
                        nuevo.izquierda = actual.izquierda
                        actual.izquierda.derecha = nuevo
                        actual.izquierda = nuevo
                        break
                    elif nuevo.x == actual.x and nuevo.y == actual.y:
                        break
                    else:
                        if actual.derecha == None:
                            actual.derecha = nuevo
                            nuevo.izquierda = actual
                            break
                        actual = actual.derecha

        # Insertar en columna
        if celda_y.acceso == None:
            celda_y.acceso = nuevo
        else:
            if nuevo.x < celda_y.acceso.x:
                nuevo.abajo = celda_y.acceso
                celda_y.acceso.arriba = nuevo
                celda_y.acceso = nuevo
            else:
                actual = celda_y.acceso
                while actual != None:
                    if nuevo.x < actual.x:
                        nuevo.abajo = actual
                        nuevo.arriba = actual.arriba
                        actual.arriba.abajo = nuevo
                        actual.arriba = nuevo
                        break
                    elif nuevo.x == actual.x and nuevo.y == actual.y:
                        break
                    else:
                        if actual.abajo == None:
                            actual.abajo = nuevo
                            nuevo.arriba = actual
                            break
                        actual = actual.abajo

    def graficar(self, id_figura):
        if not os.path.exists('./Reportes'):
            os.makedirs('./Reportes')
        if not os.path.exists('./reportesdot'):
            os.makedirs('./reportesdot')
            
        dot = 'digraph MatrizDispersa {\n'
        dot += '    node [shape=box];\n'
        dot += '    graph [rankdir=TB];\n'
        dot += '    node [width=0.5 height=0.5 fixedsize=true];\n'
        
        # Encontrar dimensiones de la matriz
        max_fila = 0
        max_col = 0
        actual_fila = self.filas.primero
        while actual_fila:
            max_fila = max(max_fila, actual_fila.id)
            actual_celda = actual_fila.acceso
            while actual_celda:
                max_col = max(max_col, actual_celda.y)
                actual_celda = actual_celda.derecha
            actual_fila = actual_fila.siguiente
        
        # Crear nodos invisibles para mantener la estructura
        for i in range(max_fila + 1):
            for j in range(max_col + 1):
                dot += f'    nodo_{i}_{j} [label="", style=invis];\n'
        
        # Crear subgrafos para cada fila para mantener el orden
        for i in range(max_fila + 1):
            dot += f'    {{rank=same; '
            for j in range(max_col + 1):
                dot += f'nodo_{i}_{j} '
            dot += '}\n'
        
        # Conectar nodos horizontalmente
        for i in range(max_fila + 1):
            for j in range(max_col):
                dot += f'    nodo_{i}_{j} -> nodo_{i}_{j+1} [style=invis];\n'
        
        # Conectar nodos verticalmente
        for j in range(max_col + 1):
            for i in range(max_fila):
                dot += f'    nodo_{i}_{j} -> nodo_{i+1}_{j} [style=invis];\n'
        
        # Agregar nodos con color
        actual_fila = self.filas.primero
        while actual_fila:
            actual_celda = actual_fila.acceso
            while actual_celda:
                dot += f'    nodo_{actual_celda.x}_{actual_celda.y} [label="", style=filled, fillcolor="{actual_celda.valor}"];\n'
                actual_celda = actual_celda.derecha
            actual_fila = actual_fila.siguiente
        
        dot += '}\n'
        
        # Guardar archivos
        dot_path = f'./reportesdot/Matriz_{id_figura}.dot'
        svg_path = f'./Reportes/Matriz_{id_figura}.svg'
        
        with open(dot_path, 'w', encoding='utf-8') as f:
            f.write(dot)
            
        os.system(f'dot -Tsvg {dot_path} -o {svg_path}')
        
        return svg_path
