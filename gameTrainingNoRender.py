import math
from matplotlib import pyplot as plt
import numpy as np
import pygame
import sys
import random

import torch
from enemy import Enemy
from getKeyGrafo import get_key
from dijkstra import dijkstra
from user import User
from item import Item
from footer import paintFooter
from square import drawSquare
from loadingScreen import loadingScreen
from pauseMenu import pauseMenu
from resultsMenu import resultsMenu
from settings import settings
from createMap import createMap
from rewardSystemPoints import rewards
from getGameData import getData

def getState(map, enemies, players, costMap):
    mapMatrix, enemiesMatrix, playersMatrix, costMapMatrix = getData(map, enemies, players, costMap)
    state = convert_to_tensor(mapMatrix, enemiesMatrix, playersMatrix, costMapMatrix)
    return state

def convert_to_tensor(matrix1, matrix2, matrix3, matrix4):
    """
    Converts four (10,10) normalized matrices into a PyTorch tensor formatted for the DQN.
    
    Parameters:
    - matrix1, matrix2, matrix3, matrix4: Normalized numpy arrays of shape (10,10).
    
    Returns:
    - PyTorch tensor of shape (1, 4, 10, 10) ready for input to the DQN.
    """
    # Stack the four matrices along the channel dimension to create (10,10,4)
    state_array = np.stack([matrix1, matrix2, matrix3, matrix4], axis=-1)  # Shape (10,10,4)

    # Convert to PyTorch tensor and format for CNN input (batch, channels, height, width)
    state_tensor = torch.tensor(state_array, dtype=torch.float32).permute(2, 0, 1)

    return state_tensor

def playMusic():
    pygame.mixer.music.load("./assets/musicGame.mp3")
    pygame.mixer.music.play(-1)


def game(seed, players_amount, enemies_amount, map_size, steps, get_action):
    pygame.init()
    # playMusic()
    random.seed(seed)
    playing = True
    globalHeight = settings["screenHeight"]
    globalWidth = settings["screenWidth"]
    # Define grid properties
    smallMapGrid = (settings["smallMapRows"], settings["smallMapCols"])
    mediumMapGrid = (settings["mediumMapRows"], settings["mediumMapCols"])
    largeMapGrid = (settings["largeMapRows"], settings["largeMapCols"])
    if map_size == "S":
        grid_rows, grid_cols = smallMapGrid[0], smallMapGrid[1]
    if map_size == "M":
        grid_rows, grid_cols = mediumMapGrid[0], mediumMapGrid[1]
    if map_size == "L":
        grid_rows, grid_cols = largeMapGrid[0], largeMapGrid[1]

    clock = pygame.time.Clock()

    ##
    lastUpdateTimes = [pygame.time.get_ticks() for _ in range(0, players_amount)]
    ##
    lastUpdateTime = pygame.time.get_ticks()
    ##

    grid = [[1 for _ in range(grid_cols)] for _ in range(grid_rows)]
    nodos = [[1 for _ in range(grid_cols)] for _ in range(grid_rows)]
    libres = []
    nuevos_puntos = True
    if map_size == "S":
        distancia_pursue = settings["pursueDistance"]
    if map_size == "M":
        distancia_pursue = settings["pursueDistance"]
    if map_size == "L":
        distancia_pursue = settings["pursueDistance"]

    spawnPoints = []
    safeZoneSpawnPoints = []
    safeZoneRightPoints = []
    safeZoneDownPoints = []
    grafo, grafoTraining = createMap(
        grid_rows,
        grid_cols,
        libres,
        grid,
        nodos,
        spawnPoints,
        safeZoneSpawnPoints,
        safeZoneRightPoints,
        safeZoneDownPoints,
    )

    enemigos = []
    for _ in range(0, enemies_amount):
        enemigos.append(Enemy(grid_rows // 2, grid_cols // 2, (255, 0, 0)))

    totalPuntos = len(libres)
    items = []
    items_posiciones = []
    items_timer = pygame.time.get_ticks()

    special_item = False
    special_item_posicion = (-1, -1)
    special_item_timer = pygame.time.get_ticks()

    user_speed = settings["userSpeed"]
    enemies_speed = settings["enemySpeed"]

    # Spawn Points copy
    spawnPointsComplete = spawnPoints.copy()
    safeZoneSpawnPointsComplete = safeZoneSpawnPoints.copy()

    jugadores = []
    for i in range(0, players_amount):
        # Get player position from spawn or safe zone
        if len(spawnPoints) > 0:
            playerPosition = random.choice(spawnPoints)
            spawnPoints.remove(playerPosition)
        else:
            if len(safeZoneSpawnPoints) > 0:
                playerPosition = random.choice(safeZoneSpawnPoints)
                safeZoneSpawnPoints.remove(playerPosition)
            else:
                if len(safeZoneRightPoints) > 0:
                    playerPosition = random.choice(safeZoneRightPoints)
                    safeZoneRightPoints.remove(playerPosition)
                else:
                    if len(safeZoneDownPoints) > 0:
                        playerPosition = random.choice(safeZoneDownPoints)
                        safeZoneDownPoints.remove(playerPosition)
                    else:
                        if len(spawnPointsComplete) > 0:
                            playerPosition = random.choice(spawnPointsComplete)
                        else:
                            playerPosition = random.choice(safeZoneSpawnPointsComplete)
        #
        jugadores.append(User(playerPosition[0], playerPosition[1], (0,0,0)))

    jugadores_posiciones = []
    for jugador in jugadores:
        jugadores_posiciones.append((jugador.row, jugador.col))

    todos_jugadores = []
    for jugador in jugadores:
        todos_jugadores.append(jugador)

    special_time_timer = pygame.time.get_ticks()
    special_time = False

    enemies_respawn_timer = pygame.time.get_ticks()

    consecutiveCollectedPoints = 0

    reward_list = []

    episode_data = []

    for _ in range(0, steps):
        (
            totalPuntos,
            nuevos_puntos,
            lastUpdateTime,
            special_item,
            special_item_posicion,
            special_time,
            special_time_timer,
            items_timer,
            special_item_timer,
            playing,
            enemies_respawn_timer,
            consecutiveCollectedPoints,
            reward,
            state,
            action,
            next_state,
            saveStepData
        ) = step(
            grid,
            grid_rows,
            grid_cols,
            todos_jugadores,
            enemies_speed,
            libres,
            items,
            enemigos,
            grafo,
            nodos,
            jugadores,
            distancia_pursue,
            lastUpdateTimes,
            user_speed,
            jugadores_posiciones,
            items_posiciones,
            enemies_amount,
            clock,
            lastUpdateTime,
            nuevos_puntos,
            totalPuntos,
            items_timer,
            special_item,
            special_item_posicion,
            special_item_timer,
            enemies_respawn_timer,
            special_time_timer,
            special_time,
            playing,
            consecutiveCollectedPoints,
            grafoTraining,
            get_action,
        )
        reward_list.append(reward)
        
        if saveStepData:
            episode_data.append((state, action, reward, next_state, playing))
        clock.tick(45)

    return episode_data
    """
    # Compute basic stats
    mean_reward = np.mean(reward_list)
    min_reward = np.min(reward_list)
    max_reward = np.max(reward_list)
    std_dev = np.std(reward_list)

    print(f"Mean Reward: {mean_reward:.3f}")
    print(f"Min Reward: {min_reward:.3f}")
    print(f"Max Reward: {max_reward:.3f}")
    print(f"Standard Deviation: {std_dev:.3f}")
    """

    """
    plt.plot(reward_list, marker="o", linestyle="-", color="b")
    plt.axhline(y=0, color="r", linestyle="--", label="Zero Reward")
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Reward Trend Over Time (Random Movement)")
    plt.legend()
    plt.show()
    """
    #

    """
    pygame.mixer.music.load("./assets/musicMenu.mp3")
    pygame.mixer.music.play(-1)
    """


def getRandomAction():
    actions = ["up", "down", "right", "left"]
    return random.choice(actions)


def step(
    grid,
    grid_rows,
    grid_cols,
    todos_jugadores,
    enemies_speed,
    libres,
    items,
    enemigos,
    grafo,
    nodos,
    jugadores,
    distancia_pursue,
    lastUpdateTimes,
    user_speed,
    jugadores_posiciones,
    items_posiciones,
    enemies_amount,
    clock,
    lastUpdateTime,
    nuevos_puntos,
    totalPuntos,
    items_timer,
    special_item,
    special_item_posicion,
    special_item_timer,
    enemies_respawn_timer,
    special_time_timer,
    special_time,
    playing,
    consecutiveCollectedPoints,
    grafoTraining,
    get_action,
):
    pacmanMoved = False
    enemiesMoved = False
    reward = rewards["stepCost"]
    if nuevos_puntos:
        totalPuntos = len(libres) - len(items)
        if special_item:
            totalPuntos -= 1
        nuevos_puntos = False

    # Calculate elapsed time since the last update
    curr_time = pygame.time.get_ticks()

    current_time = pygame.time.get_ticks()

    if current_time - lastUpdateTime > enemies_speed:
        enemiesMoved = True
        for enemigo in enemigos:
            enemigo.pursue(
                grafo,
                nodos,
                jugadores,
                enemigos,
                libres,
                distancia_pursue,
                special_time,
            )
        lastUpdateTime = current_time

    #### Get Closests Before Move
    pacmanPositionNodo = get_key(
        todos_jugadores[0].row, todos_jugadores[0].col, grid_cols
    )
    dijkstra(grafoTraining, grafoTraining[pacmanPositionNodo], enemigos)
    pacmanBeforeDijkstra = [[None for _ in range(grid_cols)] for _ in range(grid_rows)]
    for nodo in grafoTraining.values():  # Directly iterate over nodes
        nodoRow = nodo.posicion[0]
        nodoCol = nodo.posicion[1]
        pacmanBeforeDijkstra[nodoRow][nodoCol] = nodo  # Use node's properties

    enemiesClosestPositionCheck = []
    for enemy in enemigos:
        enemiesClosestPositionCheck.append(
            pacmanBeforeDijkstra[enemy.row][enemy.col].valor
        )
    minEnemyDistance = (
        min(enemiesClosestPositionCheck) if enemiesClosestPositionCheck else -1
    )

    pointsClosestPositionCheck = []
    greenPointsClosestPositionCheck = []
    specialPointsClosestPositionCheck = []
    for beforeGridRow in range(0, grid_rows):
        for beforeGridCol in range(0, grid_cols):
            if grid[beforeGridRow][beforeGridCol] == 1:
                pointsClosestPositionCheck.append(
                    pacmanBeforeDijkstra[beforeGridRow][beforeGridCol].valor
                )
            elif grid[beforeGridRow][beforeGridCol] == 3:
                greenPointsClosestPositionCheck.append(
                    pacmanBeforeDijkstra[beforeGridRow][beforeGridCol].valor
                )
            elif grid[beforeGridRow][beforeGridCol] == 4:
                specialPointsClosestPositionCheck.append(
                    pacmanBeforeDijkstra[beforeGridRow][beforeGridCol].valor
                )

    minPointDistance = (
        min(pointsClosestPositionCheck) if pointsClosestPositionCheck else -1
    )
    minGreenPointDistance = (
        min(greenPointsClosestPositionCheck) if greenPointsClosestPositionCheck else -1
    )
    minSpecialPointDistance = (
        min(specialPointsClosestPositionCheck)
        if specialPointsClosestPositionCheck
        else -1
    )
    ####
    
    state = getState(grid, enemigos, todos_jugadores, pacmanBeforeDijkstra)
    
    action = get_action(state)
    moves = ['up', 'down', 'right',' left']
    moveAction = moves[action]

    pacmanPositionChange = False
    # Use a delay to control movement speed
    for index in range(0, len(todos_jugadores)):
        player = todos_jugadores[index]
        if player.vidas > 0 and current_time - lastUpdateTimes[index] > user_speed:
            pacmanMoved = True
            if moveAction == "left":
                if player.col > 0:
                    if grid[player.row][player.col - 1] in {
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        500,
                        501,
                        502,
                    } and ((player.row, player.col - 1) not in jugadores_posiciones):
                        player.col -= 1
                        pacmanPositionChange = True
                else:
                    if player.row > distancia_pursue or player.col > distancia_pursue:
                        if grid[player.row][grid_cols - 1] in {0, 1, 2, 3, 4} and (
                            (player.row, grid_cols - 1) not in jugadores_posiciones
                        ):
                            player.col = grid_cols - 1
                            pacmanPositionChange = True
            elif moveAction == "right":
                if player.col < grid_cols - 1:
                    if grid[player.row][player.col + 1] in {
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        500,
                        501,
                        502,
                    } and ((player.row, player.col + 1) not in jugadores_posiciones):
                        player.col += 1
                        pacmanPositionChange = True
                else:
                    if grid[player.row][0] in {0, 1, 2, 3, 4} and (
                        (player.row, 0) not in jugadores_posiciones
                    ):
                        player.col = 0
                        pacmanPositionChange = True
            elif moveAction == "up":
                if player.row > 0:
                    if grid[player.row - 1][player.col] in {
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        500,
                        501,
                        502,
                    } and ((player.row - 1, player.col) not in jugadores_posiciones):
                        player.row -= 1
                        pacmanPositionChange = True
                else:
                    if player.row > distancia_pursue or player.col > distancia_pursue:
                        if grid[grid_rows - 1][player.col] in {0, 1, 2, 3, 4} and (
                            (grid_rows - 1, player.col) not in jugadores_posiciones
                        ):
                            player.row = grid_rows - 1
                            pacmanPositionChange = True
            elif moveAction == "down":
                if player.row < grid_rows - 1:
                    if grid[player.row + 1][player.col] in {
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        500,
                        501,
                        502,
                    } and ((player.row + 1, player.col) not in jugadores_posiciones):
                        player.row += 1
                        pacmanPositionChange = True
                else:
                    if grid[0][player.col] in {0, 1, 2, 3, 4} and (
                        (0, player.col) not in jugadores_posiciones
                    ):
                        player.row = 0
                        pacmanPositionChange = True
            jugadores_posiciones[index] = (player.row, player.col)
            lastUpdateTimes[index] = current_time

    if not pacmanPositionChange:
        reward += rewards["moveWall"]

    ####
    pacmanPositionNodo = get_key(
        todos_jugadores[0].row, todos_jugadores[0].col, grid_cols
    )
    dijkstra(grafoTraining, grafoTraining[pacmanPositionNodo], enemigos)
    pacmanDijkstra = [[None for _ in range(grid_cols)] for _ in range(grid_rows)]
    for nodo in grafoTraining.values():  # Directly iterate over nodes
        nodoRow = nodo.posicion[0]
        nodoCol = nodo.posicion[1]
        pacmanDijkstra[nodoRow][nodoCol] = nodo  # Use node's properties
    ###

    #### Get Closests After Move
    enemiesClosestPositionCheckAfter = []
    for enemy in enemigos:
        enemiesClosestPositionCheckAfter.append(
            pacmanDijkstra[enemy.row][enemy.col].valor
        )
    minEnemyDistanceAfter = (
        min(enemiesClosestPositionCheckAfter)
        if enemiesClosestPositionCheckAfter
        else -1
    )

    pointsClosestPositionCheckAfter = []
    greenPointsClosestPositionCheckAfter = []
    specialPointsClosestPositionCheckAfter = []
    for afterGridRow in range(0, grid_rows):
        for afterGridCol in range(0, grid_cols):
            if grid[afterGridRow][afterGridCol] == 1:
                pointsClosestPositionCheckAfter.append(
                    pacmanDijkstra[afterGridRow][afterGridCol].valor
                )
            elif grid[afterGridRow][afterGridCol] == 3:
                greenPointsClosestPositionCheckAfter.append(
                    pacmanDijkstra[afterGridRow][afterGridCol].valor
                )
            elif grid[afterGridRow][afterGridCol] == 4:
                specialPointsClosestPositionCheckAfter.append(
                    pacmanDijkstra[afterGridRow][afterGridCol].valor
                )

    minPointDistanceAfter = (
        min(pointsClosestPositionCheckAfter) if pointsClosestPositionCheckAfter else -1
    )
    minGreenPointDistanceAfter = (
        min(greenPointsClosestPositionCheckAfter)
        if greenPointsClosestPositionCheckAfter
        else -1
    )
    minSpecialPointDistanceAfter = (
        min(specialPointsClosestPositionCheckAfter)
        if specialPointsClosestPositionCheckAfter
        else -1
    )
    ####

    ##Reward distance base
    if minEnemyDistance != -1 and minEnemyDistanceAfter != -1:
        if minEnemyDistance < minEnemyDistanceAfter:
            if special_time:
                reward += rewards["moveFurtherSpecialEnemy"]
            else:
                reward += rewards["moveFurtherEnemy"]
        else:
            if special_time:
                reward += rewards["moveCloserSpecialEnemy"]
            else:
                reward += rewards["moveCloserEnemy"]

    if minPointDistance != -1 and minPointDistanceAfter != -1:
        if minPointDistance > minPointDistanceAfter:
            reward += rewards["moveCloserPoint"]

    if minGreenPointDistance != -1 and minGreenPointDistanceAfter != -1:
        if minGreenPointDistance > minGreenPointDistanceAfter:
            reward += rewards["moveCloserGreenPoint"]

    if minSpecialPointDistance != -1 and minSpecialPointDistanceAfter != -1:
        if minSpecialPointDistance > minSpecialPointDistanceAfter:
            reward += rewards["moveCloserSpecialPoint"]
    ###

    next_state = getState(grid, enemigos, todos_jugadores, pacmanBeforeDijkstra)

    # Update game state
    for jugador in jugadores:
        if grid[jugador.row][jugador.col] == 1:
            grid[jugador.row][jugador.col] = 2
            totalPuntos -= 1
            jugador.puntos += 1
            reward += rewards["point"]
            consecutiveCollectedPoints += 1
            reward += rewards["consecutivePointsCollected"] * math.log(
                consecutiveCollectedPoints
            )
            if totalPuntos == 0:
                nuevos_puntos = True
                totalPuntos = len(libres) - len(items) - 1
                if special_item:
                    totalPuntos -= 1
                jugador.puntos += 10
                reward += rewards["eatLastPoint"]

        if grid[jugador.row][jugador.col] == 2:
            reward += rewards["moveEmptySpace"]

        if grid[jugador.row][jugador.col] == 3:
            grid[jugador.row][jugador.col] = 2
            for item in items:
                if item.col == jugador.col and item.row == jugador.row:
                    items.remove(item)
            items_posiciones.remove((jugador.row, jugador.col))
            jugador.puntos += 5
            jugador.puntos2 += 1
            reward += rewards["greenPoint"]

        if grid[jugador.row][jugador.col] == 4:
            grid[jugador.row][jugador.col] = 2
            special_item = False
            special_item_posicion = (-1, -1)
            special_time = True
            # pygame.mixer.music.load("./assets/musicSpecial.mp3")
            # pygame.mixer.music.play(-1)
            special_time_timer = curr_time
            reward += rewards["specialPoint"]

        if grid[jugador.row][jugador.col] in {500, 501, 502}:
            for enemy in enemigos:
                enemyRow, enemyCol = enemy.row, enemy.col
                if (
                    pacmanDijkstra[enemyRow][enemyCol].valor
                    - grid[jugador.row][jugador.col]
                    < settings["pursueDistance"]
                ):
                    reward += rewards["safeZoneEnemyClose"]
                    break

    if special_time and ((curr_time - special_time_timer) >= 5000):
        special_time = False
        # pygame.mixer.music.load("./assets/musicGame.mp3")
        # pygame.mixer.music.play(-1)

    # Draw grid lines (optional)
    # for i in range(1, grid_cols):
    #    pygame.draw.line(screen, (128, 128, 128), (i * grid_size, 0), (i * grid_size, height))
    # for j in range(1, grid_rows):
    #    pygame.draw.line(screen, (128, 128, 128), (0, j * grid_size), (width, j * grid_size))

    items_time_passed = curr_time - items_timer

    if items_time_passed >= 5000:
        item_pos = random.choice(libres)
        if (
            item_pos != special_item_posicion
            and item_pos not in jugadores_posiciones
            and item_pos not in items_posiciones
            and grid[item_pos[0]][item_pos[1]] == 2
        ):
            items.append(Item(item_pos[0], item_pos[1], (0, 255, 0)))
            items_posiciones.append((item_pos[0], item_pos[1]))
            grid[item_pos[0]][item_pos[1]] = 3
            if len(items) == 4:
                items.pop(0)
                grid[items_posiciones[0][0]][items_posiciones[0][1]] = 2
                items_posiciones.pop(0)
        items_timer = curr_time  # Update the last update time

    special_item_time_passed = curr_time - special_item_timer

    if special_item_time_passed >= 10000:
        special_item_pos = random.choice(libres)
        if (
            len(enemigos) > 0
            and special_item == False
            and special_item_pos not in jugadores_posiciones
            and special_item_pos not in items_posiciones
            and grid[special_item_pos[0]][special_item_pos[1]] == 2
        ):
            special_item = True
            special_item_posicion = special_item_pos
            grid[special_item_pos[0]][special_item_pos[1]] = 4
        special_item_timer = curr_time  # Update the last update time

    # Draw Enemies
    for enemy in enemigos:
        for jugador in jugadores:
            if enemy.col == jugador.col and enemy.row == jugador.row:
                if not special_time:
                    # pygame.mixer.Channel(1).play(pygame.mixer.Sound("./assets/musicError.mp3"))
                    jugador.vidas -= 1
                    reward += rewards["loseLife"]
                    # pygame.mixer.Channel(1).stop()
                    if jugador.vidas != 0:
                        jugador.col = 1
                        jugador.row = 1
                    else:
                        jugadores.remove(jugador)
                        for i, pos in enumerate(jugadores_posiciones):
                            if pos == (jugador.row, jugador.col):
                                jugadores_posiciones[i] = (-1, -1)
                        # jugadores_posiciones.remove((jugador.row, jugador.col))
                        if len(jugadores) == 0:
                            playing = False
                else:
                    # pygame.mixer.Channel(2).play(pygame.mixer.Sound("./assets/musicGain.mp3"))
                    enemigos.remove(enemy)
                    # pygame.mixer.Channel(2).stop()
                    jugador.puntos += 20
                    reward += rewards["eatEnemy"]

    if (curr_time - enemies_respawn_timer) > 40000:
        for i in range(0, enemies_amount - len(enemigos)):
            enemigos.append(Enemy(grid_rows // 2, grid_cols // 2, (255, 0, 0)))
        enemies_respawn_timer = curr_time
    # Refresh the display

    if not pacmanMoved:
        reward = 0

    saveStepData = True
    if pacmanMoved or enemiesMoved:
        saveStepData = False

    return (
        totalPuntos,
        nuevos_puntos,
        lastUpdateTime,
        special_item,
        special_item_posicion,
        special_time,
        special_time_timer,
        items_timer,
        special_item_timer,
        playing,
        enemies_respawn_timer,
        consecutiveCollectedPoints,
        reward,
        state,
        action,
        next_state,
        saveStepData
    )