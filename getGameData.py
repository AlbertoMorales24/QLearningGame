import numpy as np
from dijkstra import dijkstra

np.set_printoptions(suppress=True)  # Disable scientific notation

def getData(map, enemies, players, costMatrix):
    normalizedMap = normalize_matrix(map)
    enemiesMap = create_enemy_matrix(len(map), len(map[0]), enemies)
    playersMaps = create_enemy_matrix(len(map), len(map[0]), players)
    distancesMap = [[obj.valor for obj in row] for row in costMatrix]
    normalizedDistances = normalize_matrix(distancesMap)
    
    return normalizedMap, enemiesMap, playersMaps, normalizedDistances

def getPlayerNodo(player, grafo):
    row = player.row
    col = player.col
    for nodo in grafo.values():
        if nodo.posicion == (row, col):
            return nodo

def normalize_matrix(matrix):
    """
    Normalizes a matrix to have values between 0 and 1.
    If the matrix has all zeros, it returns the original matrix to avoid division errors.
    """
    matrix = np.array(matrix, dtype=np.float32)
    max_value = np.max(matrix)

    if max_value > 0:  # Avoid division by zero
        return matrix / max_value
    else:
        return matrix  # If max_value is 0, return the original matrix
    
def create_enemy_matrix(grid_rows, grid_cols, enemies):
    """
    Creates an enemy presence matrix where:
    - `1` represents an enemy.
    - `0` represents empty space.

    Parameters:
    - grid_rows (int): Number of rows in the map.
    - grid_cols (int): Number of columns in the map.
    - enemies (list of tuples): Each tuple contains (row, col) of an enemy.

    Returns:
    - enemy_matrix (np.array): A matrix with 1s for enemies, 0s elsewhere.
    """
    # Initialize an empty matrix filled with zeros
    enemy_matrix = np.zeros((grid_rows, grid_cols), dtype=np.float32)

    # Place enemies in the matrix
    for enemy in enemies:
        row, col = enemy.row, enemy.col  # Extract row and column position
        enemy_matrix[row][col] = 1  # Set enemy position to 1

    return enemy_matrix

def create_distances_matrix(grid_rows, grid_cols, grafo):
    # Initialize an empty matrix filled with zeros
    enemy_matrix = np.zeros((grid_rows, grid_cols), dtype=np.float32)

    # Place enemies in the matrix
    for nodo in grafo.values():
        row, col = nodo.posicion[0], nodo.posicion[1]  # Extract row and column position
        enemy_matrix[row, col] = nodo.valor  # Set enemy position to 1

    return enemy_matrix
