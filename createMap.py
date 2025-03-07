import math
import random

from dijkstra import dijkstra
from getNeighbours import getNeighbours
from grafo import crearGrafo
from nodo import Nodo
from randomWall import randomWall


def createMap(grid_rows, grid_cols, libres, grid, nodos, spawnPoints, safeZoneSpawnPoints, safeZoneRightPoints, safeZoneDownPoints):
    spawnRows = math.ceil(grid_rows * 0.1)
    spawnCols = math.ceil(grid_cols * 0.1)
    safeZoneSpawn = []
    safeZoneRight = []
    safeZoneDown = []
    ### Create Map
    for i in range(0, grid_rows):
        for j in range(0, grid_cols):
            libres.append((i,j))
            if i < grid_rows * 0.1 and j < grid_cols * 0.1 and i != 0 and j != 0:
                #Spawn
                grid[i][j] = 5
                libres.pop()
                spawnPoints.append((i,j))
            #Zona Segura (Abajo, Derecha, Izquierda, Arriba)
            elif (i == spawnRows and j <= spawnCols) or (j == spawnCols and i < spawnRows) or (i <= spawnRows and j == 0) or (j <= spawnCols and i == 0):
                if grid[i][j] != 5:
                    libres.pop()
                #Zona Segura Spawn
                grid[i][j] = 500
                safeZoneSpawn.append((i,j))
            elif (i <= spawnRows and j == grid_cols-1):
                #Zona Segura Derecha
                grid[i][j] = 501
                safeZoneRight.append((i,j))
                libres.pop()
            elif (i == grid_rows-1 and j <= spawnCols):
                #Zona Segura Abajo
                grid[i][j] = 502
                safeZoneDown.append((i,j))
                libres.pop()
            else:
                if i != grid_rows//2 and j != grid_cols//2:
                    if getNeighbours(grid, grid_rows, grid_cols, i,j, True) > 2:
                        if (i == spawnRows+1 and j <= spawnCols+1) or (j == spawnCols+1 and i < spawnRows+1) or (i <= spawnRows+1 and j == grid_cols-1-1) or (i <= spawnRows+1 and j == grid_cols-1) or (i == grid_rows-1-1 and j <= spawnCols+1) or (i == grid_rows-1 and j <= spawnCols+1):
                            # Walls next to Spawn
                            """ if randomWall():
                                grid[i][j] = 1000
                                libres.pop() """
                            pass
                        else:
                            if randomWall():
                                grid[i][j] = 1000
                                libres.pop()
                if i == grid_rows//2 and j == grid_cols//2:
                    #Libre Medio
                    grid[i][j] = 0
                    libres.pop()
            nodos[i][j] = Nodo((i,j))
    
    ## Safe Safe Zone Points
    safeZoneSpawnPoints[:] = safeZoneSpawn.copy()
    safeZoneRightPoints[:] = safeZoneRight.copy()
    safeZoneDownPoints[:] = safeZoneDown.copy()
            
    #### Open Safe Zones Paths
    #Spawn Safe Zone Path
    safeZoneSpawnInit = random.choice(safeZoneSpawn)
    safeZoneSpawnInitRow = safeZoneSpawnInit[0]
    safeZoneSpawnInitCol = safeZoneSpawnInit[1]
    safeZoneSpawnDirection = random.randint(0,1)
    if safeZoneSpawnDirection == 0:
        for i in range(safeZoneSpawnInitRow, grid_rows // 2):
            if grid[i][safeZoneSpawnInitCol] == 1000:
                grid[i][safeZoneSpawnInitCol] = 1
                libres.append((i, safeZoneSpawnInitCol))
    else:
        for i in range(safeZoneSpawnInitCol, grid_cols // 2):
            if grid[safeZoneSpawnInitRow][i] == 1000:
                grid[safeZoneSpawnInitRow][i] = 1
                libres.append((safeZoneSpawnInitRow, i))
    ####
    #Right Safe Zone Path
    safeZoneRightInit = random.choice(safeZoneRight)
    safeZoneRightInitRow = safeZoneRightInit[0]
    safeZoneRightInitCol = safeZoneRightInit[1]
    safeZoneRightDirection = random.randint(0,1)
    if safeZoneRightDirection == 0:
        for i in range(safeZoneRightInitRow, grid_rows // 2):
            if grid[i][safeZoneRightInitCol] == 1000:
                grid[i][safeZoneRightInitCol] = 1
                libres.append((i, safeZoneRightInitCol))
    else:
        for i in range(grid_cols // 2, safeZoneRightInitCol):
            if grid[safeZoneRightInitRow][i] == 1000:
                grid[safeZoneRightInitRow][i] = 1
                libres.append((safeZoneRightInitRow, i))
    ####
    #Down Safe Zone Path
    safeZoneDownInit = random.choice(safeZoneDown)
    safeZoneDownInitRow = safeZoneDownInit[0]
    safeZoneDownInitCol = safeZoneDownInit[1]
    safeZoneDownDirection = random.randint(0,1)
    if safeZoneDownDirection == 0:
        for i in range(grid_rows // 2, safeZoneDownInitRow):
            if grid[i][safeZoneDownInitCol] == 1000:
                grid[i][safeZoneDownInitCol] = 1
                libres.append((i, safeZoneDownInitCol))
    else:
        for i in range(safeZoneDownInitCol, grid_cols // 2):
            if grid[safeZoneDownInitRow][i] == 1000:
                grid[safeZoneDownInitRow][i] = 1
                libres.append((safeZoneDownInitRow, i))
    ####
                
    grafo = crearGrafo(nodos, grid, grid_rows, grid_cols)

    dijkstra(grafo, nodos[grid_rows//2][grid_cols//2], [])
    # Close closed areas
    for i in range(0, grid_rows):
        for j in range(0, grid_cols):
            if grid[i][j] == 1:
                if nodos[i][j].valor > 800:
                    grid[i][j] = 1000
                    libres.remove((i,j))
                    grafo = crearGrafo(nodos, grid, grid_rows, grid_cols)
                    dijkstra(grafo, nodos[grid_rows//2][grid_cols//2], [])
    
    nodosTraining = [[Nodo(nodos[i][j].posicion) for j in range(grid_cols)] for i in range(grid_rows)]
    grafoTraining = crearGrafo(nodosTraining, grid, grid_rows, grid_cols)
    
    return grafo, grafoTraining