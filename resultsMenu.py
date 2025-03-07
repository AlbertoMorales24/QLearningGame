import sys
import pygame

from square import drawSquare


def resultsMenu(screen, width, height, total_jugadores, jugadores):
    paused = True
    while paused:
        # Define the rectangle dimensions
        if width <= 200:
            width_factor = 0.8
        else:
            width_factor = 0.5
            
        if height <= 200:
            height_factor = 0.6
        else:
            height_factor = 0.5
        menu_width, menu_height = width * width_factor, height * height_factor

        # Calculate the position of the top-left corner of the rectangle
        menu_x = (width - menu_width) // 2
        menu_y = (height - menu_height) // 2

        # Add a background color to the menu
        menu_color = (50, 50, 50)  # Adjust the color as needed
        pygame.draw.rect(screen, menu_color, (menu_x, menu_y, menu_width, menu_height))

        # Define the title dimensions and position
        font_size = int(min(menu_width / 10, menu_height / 5) * 1)
        title_text = "Results"
        title_text_surface = pygame.font.Font(None, font_size).render(title_text, True, (255, 255, 255))
        title_y = menu_y * 1.2
        title_text_rect = title_text_surface.get_rect(center=(width // 2, title_y))

        # Draw the title
        screen.blit(title_text_surface, title_text_rect)

        cols = total_jugadores + 2
        current_col = 1
        rows = 2
        current_row = 0
        cell_width = menu_width // cols
        cell_height = (menu_height * 0.5) // rows
        font_size = int(min(cell_width / 10, cell_height / 5) * 3)

        for jugador in jugadores:
            x = current_col * cell_width + menu_x
            y = current_row * cell_height + title_y * 1.3  # Adjusted to remove unnecessary parentheses

            cell_color = (100, 100, 100)  # Adjust the color as needed
            pygame.draw.rect(screen, cell_color, (x, y, cell_width, cell_height))

            # Draw a square in the center of the cell
            square_size = min(cell_width, cell_height) * 0.8
            square_x = x + (cell_width) // 2
            square_y = y + (cell_height) // 2
            drawSquare(screen, square_x, square_y, square_size, "right", True, jugador.color)

            # Draw Points
            y += cell_height  # Adjusted to move to the next row

            text1 = "Points: " + str(jugador.puntos)
            font = pygame.font.Font(None, font_size)
            text1_surface = font.render(text1, True, (255, 255, 255))
            text1_rect = text1_surface.get_rect(center=(x + cell_width // 2, y + cell_height // 4))
            screen.blit(text1_surface, text1_rect)

            current_col += 1.2
            current_row = 0  # Reset current_row for the next iteration
        
        # Define button dimensions
        button_width, button_height = menu_width // 2, menu_height * 0.1

        # Calculate button positions
        button1_x = (width - button_width) // 2
        button1_y = menu_y + menu_height - menu_height*0.2
        
        # Draw buttons
        pygame.draw.rect(screen, (0, 255, 0), (button1_x, button1_y, button_width, button_height))

        # Render and draw text on buttons
        font_size = int(min(cell_width / 10, cell_height / 5) * 3)
        button_font = pygame.font.Font(None, font_size)
        button1_text = button_font.render("Main Menu", True, (0, 0, 0))
        
        # Calculate the position to center the text within the button
        text_x = button1_x + (button_width - button1_text.get_width()) // 2
        text_y = button1_y + (button_height - button1_text.get_height()) // 2
        
        screen.blit(button1_text, (text_x, text_y))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if mouse click is within the boundaries of the buttons
                if (
                    button1_x <= mouse_x <= button1_x + button_width
                    and button1_y <= mouse_y <= button1_y + button_height
                ):
                    paused = False

        # Update the display
        pygame.display.flip()