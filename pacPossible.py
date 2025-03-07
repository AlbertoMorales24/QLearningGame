import math
import pygame
import sys
import random
from button import Button
from enemy import Enemy
from nodo import Nodo
from dijkstra import dijkstra
from grafo import crearGrafo
from randomAction import getRandomAction
from user import User
from item import Item
from footer import paintFooter
from square import drawSquare
from loadingScreen import loadingScreen
from pauseMenu import pauseMenu
from resultsMenu import resultsMenu
from randomWall import randomWall
from getNeighbours import getNeighbours
from settings import settings
from createMap import createMap

def playMusic():
    pygame.mixer.music.load("./assets/musicGame.mp3")
    pygame.mixer.music.play(-1)

def game(seed, players_amount, bots_amount, enemies_amount, map_size):
    #playMusic()
    seed = random.randint(0,10000)
    print(seed)
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
    # Calculate the maximum grid_size that fits BOTH width and height
    grid_size_width = globalWidth // grid_cols
    grid_size_height = int(globalHeight / (grid_rows * 1.2))  # 1.2 accounts for extra UI space
    grid_size = min(grid_size_width, grid_size_height)

    # Ensure grid_size is at least 1 (avoid division by zero)
    grid_size = max(grid_size, 1)

    # Compute final screen dimensions
    width = grid_size * grid_cols
    height = int(grid_size * grid_rows * 1.2)  # Convert to integer for Pygame
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PacMan")

    clock = pygame.time.Clock()

    loadingScreen(screen, width, height)

    # Define circle properties
    circle_radius = grid_size//2
    circle_row, circle_col = 0, 0
    circle_x, circle_y = circle_col * grid_size + grid_size // 2, circle_row * grid_size + grid_size // 2

    ##
    lastUpdateTimes = [pygame.time.get_ticks() for _ in range(0, players_amount + bots_amount)]
    ##
    lastUpdateTime = pygame.time.get_ticks()
    ##

    grid = [[1 for _ in range(grid_cols)] for _ in range(grid_rows)]
    nodos = [[1 for _ in range(grid_cols)] for _ in range(grid_rows)]
    libres = []
    nuevos_puntos = True
    if map_size == "S":
        distancia_pursue = settings['pursueDistance']
    if map_size == "M":
        distancia_pursue = settings['pursueDistance']
    if map_size == "L":
        distancia_pursue = settings['pursueDistance']
    
    spawnPoints = []
    safeZoneSpawnPoints = []
    safeZoneRightPoints = []
    safeZoneDownPoints = []
    grafo, grafoNull = createMap(grid_rows, grid_cols, libres, grid, nodos, spawnPoints, safeZoneSpawnPoints, safeZoneRightPoints, safeZoneDownPoints)
    
    enemigos = []
    for i in range(0,enemies_amount):
        enemigos.append(Enemy(grid_rows//2, grid_cols//2, (255,0,0)))

    mouth_timer = pygame.time.get_ticks()
    mouth = True
    totalPuntos = len(libres)
    items = []
    items_posiciones = []
    items_timer = pygame.time.get_ticks()
    
    special_item = False
    special_item_posicion = (-1,-1)
    special_item_timer = pygame.time.get_ticks()

    user_speed = settings['userSpeed']
    enemies_speed = settings['enemySpeed']

    #Spawn Points copy
    spawnPointsComplete = spawnPoints.copy()
    safeZoneSpawnPointsComplete = safeZoneSpawnPoints.copy()

    jugadores =[]
    player1Color = settings['player1Color']
    player2Color = settings['player2Color']
    player3Color = settings['player3Color']
    player_colors = [player1Color, player2Color, player3Color]
    for i in range(0, players_amount + bots_amount):
        if len(player_colors)!=0:
            # Get a random element from the list
            rand_color = random.choice(player_colors)
            # Remove the random element from the list
            player_colors.remove(rand_color)
        else:
            rand_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        
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
        jugadores.append(User(playerPosition[0], playerPosition[1], rand_color))
        
    jugadores_posiciones = []
    for jugador in jugadores:
        jugadores_posiciones.append((jugador.row,jugador.col))

    todos_jugadores = []
    for jugador in jugadores:
        todos_jugadores.append(jugador)
        
    special_colors = [
        (255, 0, 0),     # Red
        (255, 165, 0),   # Orange
        (255, 255, 0),   # Yellow
        (0, 255, 0),     # Green
        (0, 0, 255),     # Blue
        (75, 0, 130),    # Indigo
        (148, 0, 211),   # Violet
        (255, 182, 193), # Pink
        (0, 255, 255),   # Cyan
        (128, 0, 128)    # Purple
    ]

    special_time_timer = pygame.time.get_ticks()
    special_time = False

    enemies_respawn_timer = pygame.time.get_ticks()    

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pauseMenu(screen, width, height):
                        playing = False
                
        screen.fill((255, 255, 255))  # Clear the screen
        
        #Paint Footer
        paintFooter(screen, grid_size, grid_rows, grid_cols, len(todos_jugadores), todos_jugadores)
        # Paint Grid
        for i in range(0,grid_rows):
            for j in range(0, grid_cols):
                # Calculate the center of the cell
                cell_center_x = j * grid_size + grid_size // 2
                cell_center_y = i * grid_size + grid_size // 2
                
                # Spawn
                if grid[i][j] == 5:
                    pygame.draw.rect(screen, (153, 153, 255), (j*grid_size, i*grid_size, grid_size, grid_size))
                # Punto Recogido
                if grid[i][j] == 2:
                    pygame.draw.rect(screen, (255, 255, 255), (j*grid_size, i*grid_size, grid_size, grid_size))
                # Zona Segura Spawn
                if grid[i][j] == 500:
                    pygame.draw.rect(screen, (154, 225, 249), (j*grid_size, i*grid_size, grid_size, grid_size))
                # Zona Segura Derecha
                if grid[i][j] == 501:
                    pygame.draw.rect(screen, (0, 0, 255), (j*grid_size, i*grid_size, grid_size, grid_size))
                # Zona Segura Abajo
                if grid[i][j] == 502:
                    pygame.draw.rect(screen, (0, 0, 127), (j*grid_size, i*grid_size, grid_size, grid_size))
                # Pared
                if grid[i][j] == 1000:
                    pygame.draw.rect(screen, (0, 0, 0), (j*grid_size, i*grid_size, grid_size, grid_size))
                if nuevos_puntos or grid[i][j] == 1:
                    # Draw a circle in the center of the cell
                    if nuevos_puntos and grid[i][j] not in {1000,0,3,4,5,500, 501, 502}:
                        grid[i][j] = 1
                    # Punto naranja
                    pygame.draw.circle(screen, (255, 165, 0), (cell_center_x, cell_center_y), circle_radius//2)
                # Punto verde
                if grid[i][j] == 3:
                    pygame.draw.circle(screen, (0, 255, 0), (cell_center_x, cell_center_y), circle_radius//2)
                # Punto multicolor
                if grid[i][j] == 4:
                    pygame.draw.circle(screen, random.choice(special_colors), (cell_center_x, cell_center_y), circle_radius//2)
                # Punto centro
                if grid[i][j] == 0:
                    pygame.draw.circle(screen, (100,100,100), (cell_center_x, cell_center_y), circle_radius//2)
        if nuevos_puntos:
            totalPuntos = len(libres)-len(items)
            if special_item:
                totalPuntos-=1
            nuevos_puntos = False
        
        # Calculate elapsed time since the last update
        curr_time = pygame.time.get_ticks()
        time_pased = curr_time - mouth_timer

        # Update the variable every 2 seconds
        if time_pased >= 200:  # 2000 milliseconds = 2 seconds
            mouth = not mouth
            mouth_timer = curr_time  # Update the last update time

        # Handle player input
        keys = pygame.key.get_pressed()
        usersKeys = [
            {"left": keys[pygame.K_LEFT], "right": keys[pygame.K_RIGHT], "up": keys[pygame.K_UP], "down": keys[pygame.K_DOWN]},
            {"left": keys[pygame.K_a], "right": keys[pygame.K_d], "up": keys[pygame.K_w], "down": keys[pygame.K_s]},
            {"left": keys[pygame.K_h], "right": keys[pygame.K_k], "up": keys[pygame.K_u], "down": keys[pygame.K_j]}
        ]
        
        # Add extra players userKeys
        while len(usersKeys) < players_amount:
           usersKeys.append({"left": None, "right": None, "up": None, "down": None}) 
        #
        
        current_time = pygame.time.get_ticks()

        if current_time - lastUpdateTime > enemies_speed:
            for enemigo in enemigos:
                enemigo.pursue(grafo, nodos, jugadores, enemigos, libres, distancia_pursue, special_time)
            lastUpdateTime = current_time

        # Use a delay to control movement speed
        for index in range(0,players_amount):
            player = todos_jugadores[index]
            if player.vidas>0 and current_time - lastUpdateTimes[index] > user_speed:
                        if usersKeys[index]["left"]:
                            player.orientation = "left"
                            if player.col > 0:
                                if grid[player.row][player.col-1] in {0,1,2,3,4,5,500,501,502} and ((player.row,player.col-1) not in jugadores_posiciones):
                                    player.col -= 1
                            else:
                                if player.row > distancia_pursue or player.col > distancia_pursue:
                                    if grid[player.row][grid_cols-1] in {0,1,2,3,4} and ((player.row,grid_cols-1) not in jugadores_posiciones):
                                        player.col = grid_cols-1
                        elif usersKeys[index]["right"]:
                            player.orientation = "right"
                            if player.col < grid_cols - 1:
                                if grid[player.row][player.col+1] in {0,1,2,3,4,5,500,501,502} and ((player.row,player.col+1) not in jugadores_posiciones):
                                    player.col += 1
                            else:
                                if grid[player.row][0] in {0,1,2,3,4} and ((player.row,0) not in jugadores_posiciones):
                                    player.col = 0
                        elif usersKeys[index]["up"]:
                            player.orientation = "top"
                            if player.row > 0:
                                if grid[player.row-1][player.col] in {0,1,2,3,4,5,500,501,502} and ((player.row-1,player.col) not in jugadores_posiciones):
                                    player.row -= 1
                            else:
                                if player.row > distancia_pursue or player.col > distancia_pursue:
                                    if grid[grid_rows-1][player.col] in {0,1,2,3,4} and ((grid_rows-1,player.col) not in jugadores_posiciones):
                                        player.row = grid_rows-1
                        elif usersKeys[index]["down"]:
                            player.orientation = "bottom"
                            if player.row < grid_rows - 1:
                                if grid[player.row+1][player.col] in {0,1,2,3,4,5,500,501,502} and ((player.row+1,player.col) not in jugadores_posiciones):
                                    player.row += 1
                            else:
                                if grid[0][player.col] in {0,1,2,3,4}  and ((0,player.col) not in jugadores_posiciones):
                                    player.row = 0
                        jugadores_posiciones[index] = (player.row,player.col)
                        lastUpdateTimes[index] = current_time
                        
        # Use a delay to control movement speed
        for index in range(players_amount, players_amount+bots_amount):
            player = todos_jugadores[index]
            if player.vidas>0 and current_time - lastUpdateTimes[index] > user_speed:
                        if getRandomAction() == 'left':
                            player.orientation = "left"
                            if player.col > 0:
                                if grid[player.row][player.col-1] in {0,1,2,3,4,5,500,501,502} and ((player.row,player.col-1) not in jugadores_posiciones):
                                    player.col -= 1
                            else:
                                if player.row > distancia_pursue or player.col > distancia_pursue:
                                    if grid[player.row][grid_cols-1] in {0,1,2,3,4} and ((player.row,grid_cols-1) not in jugadores_posiciones):
                                        player.col = grid_cols-1
                        elif getRandomAction() == 'right':
                            player.orientation = "right"
                            if player.col < grid_cols - 1:
                                if grid[player.row][player.col+1] in {0,1,2,3,4,5,500,501,502} and ((player.row,player.col+1) not in jugadores_posiciones):
                                    player.col += 1
                            else:
                                if grid[player.row][0] in {0,1,2,3,4} and ((player.row,0) not in jugadores_posiciones):
                                    player.col = 0
                        elif getRandomAction() == 'up':
                            player.orientation = "top"
                            if player.row > 0:
                                if grid[player.row-1][player.col] in {0,1,2,3,4,5,500,501,502} and ((player.row-1,player.col) not in jugadores_posiciones):
                                    player.row -= 1
                            else:
                                if player.row > distancia_pursue or player.col > distancia_pursue:
                                    if grid[grid_rows-1][player.col] in {0,1,2,3,4} and ((grid_rows-1,player.col) not in jugadores_posiciones):
                                        player.row = grid_rows-1
                        elif getRandomAction() == 'down':
                            player.orientation = "bottom"
                            if player.row < grid_rows - 1:
                                if grid[player.row+1][player.col] in {0,1,2,3,4,5,500,501,502} and ((player.row+1,player.col) not in jugadores_posiciones):
                                    player.row += 1
                            else:
                                if grid[0][player.col] in {0,1,2,3,4}  and ((0,player.col) not in jugadores_posiciones):
                                    player.row = 0
                        jugadores_posiciones[index] = (player.row,player.col)
                        lastUpdateTimes[index] = current_time
        
        # Update game state
        for jugador in jugadores:
            # Map grid position to screen coordinates
            circle_x = jugador.col * grid_size + grid_size // 2
            circle_y = jugador.row * grid_size + grid_size // 2

            # Draw the circle
            drawSquare(screen, circle_x, circle_y, circle_radius*1.8, jugador.orientation, mouth, jugador.color)
            #pygame.draw.circle(screen, (0, 0, 255), (circle_x, circle_y), circle_radius)

            if grid[jugador.row][jugador.col] == 1:
                grid[jugador.row][jugador.col] = 2
                totalPuntos -= 1
                jugador.puntos += 1
                if totalPuntos == 0:
                    nuevos_puntos = True
                    totalPuntos = len(libres)-len(items)-1
                    if special_item:
                        totalPuntos-=1
                    jugador.puntos += 10
                
            if grid[jugador.row][jugador.col] == 3:
                grid[jugador.row][jugador.col] = 2
                for item in items:
                    if item.col == jugador.col and item.row == jugador.row:
                        items.remove(item)
                items_posiciones.remove((jugador.row,jugador.col))
                jugador.puntos += 5
                jugador.puntos2 += 1
            
            if grid[jugador.row][jugador.col] == 4:
                grid[jugador.row][jugador.col] = 2
                special_item = False
                special_item_posicion = (-1,-1)
                special_time = True
                pygame.mixer.music.load("./assets/musicSpecial.mp3")
                pygame.mixer.music.play(-1)
                special_time_timer = curr_time
          
        if special_time and ((curr_time - special_time_timer) >= 5000):
            special_time = False
            pygame.mixer.music.load("./assets/musicGame.mp3")
            pygame.mixer.music.play(-1)
            
        # Draw grid lines (optional)
        #for i in range(1, grid_cols):
        #    pygame.draw.line(screen, (128, 128, 128), (i * grid_size, 0), (i * grid_size, height))
        #for j in range(1, grid_rows):
        #    pygame.draw.line(screen, (128, 128, 128), (0, j * grid_size), (width, j * grid_size))

        items_time_passed = curr_time - items_timer

        if items_time_passed >= 5000:
            item_pos = random.choice(libres)
            if item_pos != special_item_posicion and item_pos not in jugadores_posiciones and item_pos not in items_posiciones and grid[item_pos[0]][item_pos[1]] == 2:
                items.append(Item(item_pos[0],item_pos[1],(0,255,0)))
                items_posiciones.append((item_pos[0],item_pos[1]))
                grid[item_pos[0]][item_pos[1]] = 3
                if len(items) == 4:
                    items.pop(0)
                    grid[items_posiciones[0][0]][items_posiciones[0][1]] = 2
                    items_posiciones.pop(0)
            items_timer = curr_time  # Update the last update time
            
        special_item_time_passed = curr_time - special_item_timer

        if special_item_time_passed >= 10000:
            special_item_pos = random.choice(libres)
            if len(enemigos)>0 and special_item == False and special_item_pos not in jugadores_posiciones and special_item_pos not in items_posiciones and grid[special_item_pos[0]][special_item_pos[1]] == 2:
                special_item = True
                special_item_posicion = special_item_pos
                grid[special_item_pos[0]][special_item_pos[1]] = 4
            special_item_timer = curr_time  # Update the last update time

        # Draw Enemies
        for enemy in enemigos:
            # Map grid position to screen coordinates
            enemy_x = enemy.col * grid_size + grid_size // 2
            enemy_y = enemy.row * grid_size + grid_size // 2
            #pygame.draw.circle(screen, (255, 0, 0), (enemy_x, enemy_y), circle_radius)
            enemy.drawEnemy(screen, (enemy_x, enemy_y), circle_radius*0.8, special_time)
            for jugador in jugadores:    
                if enemy.col == jugador.col and enemy.row == jugador.row:
                    if not special_time:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./assets/musicError.mp3"))
                        jugador.vidas -= 1
                        pygame.mixer.Channel(1).stop()
                        if jugador.vidas != 0:
                            jugador.col = 1
                            jugador.row = 1
                        else:
                            jugadores.remove(jugador)
                            for i, pos in enumerate(jugadores_posiciones):
                                if pos == (jugador.row, jugador.col):
                                    jugadores_posiciones[i] = (-1, -1)
                            #jugadores_posiciones.remove((jugador.row, jugador.col))
                            if len(jugadores) == 0:
                                paintFooter(screen, grid_size, grid_rows, grid_cols, len(todos_jugadores), todos_jugadores)
                                playing = False
                                resultsMenu(screen, width, height, len(todos_jugadores), todos_jugadores)
                    else:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound("./assets/musicGain.mp3"))
                        enemigos.remove(enemy)
                        pygame.mixer.Channel(2).stop()
                        jugador.puntos += 20
                            
        if (curr_time - enemies_respawn_timer) > 40000:
            for i in range(0, enemies_amount - len(enemigos)):
                enemigos.append(Enemy(grid_rows//2, grid_cols//2, (255,0,0)))
            enemies_respawn_timer = curr_time
        # Refresh the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(45)
    #
    pygame.mixer.music.load("./assets/musicMenu.mp3")
    pygame.mixer.music.play(-1)
    
pygame.init()
game(420, 3,0, 1, "S")