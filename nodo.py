import copy
import random
from dijkstra import dijkstra

class Nodo:
    def __init__(self, posicion):
        self.posicion = posicion
        self.conexiones = {}
        self.valor = float('inf')
        self.nodoAnterior = None

    def agregarConexion(self, nodo, peso):
        self.conexiones[nodo] = peso
        
    def getNext(self, grafo, nodoFinal, enemies, libres, nodos, users, enemigo, distancia_pursue, special):
        dijkstra(grafo, self, enemies)
        if enemigo.destination == None or (enemigo.row == enemigo.destination[0] and enemigo.col == enemigo.destination[1]):
            enemigo.destination = random.choice(libres)
        jugador_cercano = None
        for jugador in users:
            user = nodos[jugador.row][jugador.col]
            if jugador_cercano is None or jugador_cercano.valor >= user.valor:
                jugador_cercano = user
        user = jugador_cercano
        if user.valor > distancia_pursue or special:
            destino = enemigo.destination
            current_node = nodos[destino[0]][destino[1]]
        else:
            current_node = user
        
        shortest_path = []
        while current_node:
            shortest_path.insert(0, current_node.posicion)
            current_node = current_node.nodoAnterior
        if len(shortest_path)>1:
            return shortest_path[1]
        return shortest_path[0]