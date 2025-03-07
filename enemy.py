import random
import pygame

class Enemy:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.destination = None
    
    def pursue(self, grafo, nodos, users, enemies, libres, distancia_pursue, special):
        nextNode = nodos[self.row][self.col].getNext(grafo, users, enemies, libres, nodos, users, self, distancia_pursue, special)
        self.row = nextNode[0]
        self.col = nextNode[1]

    def drawEnemy(self, screen, center, radius, special):
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
        if special:
            color = random.choice(special_colors)
            pygame.draw.rect(screen, color, (center[0]-radius//2, center[1]-radius//2, radius, radius*1.8))  # Body
            color = random.choice(special_colors)
            pygame.draw.circle(screen, color, center, radius)  # Head
            color = random.choice(special_colors)
            pygame.draw.circle(screen, color, (center[0]-radius//2, center[1]), radius//4)  # Left eye
            color = random.choice(special_colors)
            pygame.draw.circle(screen, color, (center[0]+radius//2, center[1]), radius//4)  # Left eye
        else:
            pygame.draw.rect(screen, (255,0,0), (center[0]-radius//2, center[1]-radius//2, radius, radius*1.8))  # Body
            pygame.draw.circle(screen, (240,190,180), center, radius)  # Head
            pygame.draw.circle(screen, (0,0,0), (center[0]-radius//2, center[1]), radius//4)  # Left eye
            pygame.draw.circle(screen, (0,0,0), (center[0]+radius//2, center[1]), radius//4)  # Left eye