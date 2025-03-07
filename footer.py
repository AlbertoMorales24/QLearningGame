import pygame

from square import drawSquare
from font import getNoneFont

def paintFooter(screen, grid_size, grid_rows, grid_cols, total_jugadores, jugadores):
    pygame.draw.rect(screen, (0,0,0), (0, grid_size * grid_rows, grid_size * grid_cols, grid_size * grid_rows * 0.2))
    # Draw the black border
    pygame.draw.rect(screen, (255,0,0), (0, grid_size * grid_rows, grid_size * grid_cols, grid_size * grid_rows * 0.2), 2)

    rows = 5
    current_row = 1
    cols = total_jugadores + 2
    current_col = 1
    cell_width = (grid_size*grid_cols) // cols
    cell_height = (grid_size * grid_rows * 0.2) // rows
    font_size = int(min(cell_width / 10, cell_height / 5) * 5)
    for jugador in jugadores:
        x = current_col * cell_width
        y = current_row * cell_height + (grid_size * grid_rows)
        # Draw a square in the center of the cell
        square_size = min(cell_width, cell_height) * 1.2
        square_x = x + (cell_width) // 2
        square_y = y + (cell_height) // 2
        drawSquare(screen, square_x, square_y, square_size, jugador.orientation, True, jugador.color)
        #pygame.draw.rect(screen, jugador.color, (square_x, square_y, square_size, square_size))
        current_row += 1
        # Draw a string in the center of the cell
        y = current_row * cell_height + (grid_size * grid_rows)
        text1 = "Points: " + str(jugador.puntos)
        font = getNoneFont(text1, cell_width*0.9, cell_height*0.9)
        text1_surface = font.render(text1, True, (255, 255, 255))
        text1_rect = text1_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
        screen.blit(text1_surface, text1_rect)
        current_row += 1
        # Draw a string in the center of the cell
        y = current_row * cell_height + (grid_size * grid_rows)
        text2 = "Lifes: " + str(jugador.vidas)
        font = getNoneFont(text2, cell_width*0.9, cell_height*0.9)
        text2_surface = font.render(text2, True, (255, 255, 255))
        text2_rect = text2_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
        screen.blit(text2_surface, text2_rect)
        
        current_col += 1
        current_row = 1