def dijkstra(grafo, nodoInicial, enemies):
    nodoInicial.valor = 0
    nodosAbiertos = list(grafo.values())
    for nodo in nodosAbiertos:
        nodo.nodoAnterior = None
        if nodo != nodoInicial:
            nodo.valor = float('inf')
    nodosCerrados = []

    while nodosAbiertos:
        nodoActivo = min(nodosAbiertos, key=lambda node: node.valor)
        nodosAbiertos.remove(nodoActivo)
        nodosCerrados.append(nodoActivo)

        for nodo, peso in nodoActivo.conexiones.items():
            distancia = nodoActivo.valor + peso
            
            # Check if the target node is occupied by an enemy
            for enemy in enemies:
                if enemy.row == nodo.posicion[0] and enemy.col == nodo.posicion[1]:
                    # Increase the weight for the node if an enemy is present
                    distancia += 100
            
            if distancia < nodo.valor:
                nodo.valor = distancia
                nodo.nodoAnterior = nodoActivo