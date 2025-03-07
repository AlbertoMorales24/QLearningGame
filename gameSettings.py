import sys
import pygame
from settings import settings
from font import getNoneFont

def setGame():
    # Set up display
    width, height = settings['screenWidth'], settings['screenHeight']
    minSize = min(width, height)
    window = pygame.display.set_mode((width, height))
    
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    # Font for title, labels, and button
    font_title = getNoneFont("Game Setting", minSize*0.9, minSize*0.9)
    font_start_button = getNoneFont("Start Game", minSize*0.5, minSize*0.5)
    fomt_back_button = getNoneFont("Back", minSize*0.15, minSize*0.15)
    
    # Main title
    title_text = font_title.render("Game Settings", True, black)
    title_rect = title_text.get_rect(center=(width // 2, height//10))
    
    # Row labels
    row_labels = ["Players", "Enemies", "Map Size"]
    font_labels = [getNoneFont(label, minSize*0.3, minSize*0.3) for label in row_labels]
    row_label_texts = [font_labels[index].render(label, True, black) for index, label in enumerate(row_labels)]
    
    # Start Button
    button_text = font_start_button.render("Start Game", True, black)
    button_width, button_height = button_text.get_width() * 1.3, button_text.get_height() * 1.4
    button_x = (width - button_width) // 2
    button_y = height * 0.9 - button_height 
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Back button
    back_button_text = fomt_back_button.render("Back", True, black)
    back_button_width, back_button_height = back_button_text.get_width() * 1.3, back_button_text.get_height() * 1.4
    back_button_x, back_button_y = width // 50, height // 50
    back_button_rect = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)
    
    # Square data
    square_size = minSize * 0.1
    padding = square_size * 0.2
    squares = []  # List to store information about each square
    
    for i in range(3):
        row_squares = []
        for j in range(3):
            square_rect = pygame.Rect(0, 0, square_size, square_size)
            square_rect.x = j * (square_size + padding) + (width - 3 * (square_size + padding)) // 2
            square_rect.y = height // 4 + i * (height // 5) + padding
            row_squares.append(square_rect)
        squares.append(row_squares)
    
    # Main loop
    running = True
    startGame = False
    map_sizes = ["S", "M", "L"]
    actives = [[True, False, False], [True, False, False], [True, False, False]]
    players = 1
    enemies = 0
    size = "S"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the click is within the back button rectangle
                    if back_button_rect.collidepoint(event.pos):
                        running = False
                    elif button_rect.collidepoint(event.pos):
                        running = False
                        startGame = True
                    else:
                        for i, row in enumerate(squares):
                            for j, square_rect in enumerate(row):
                                if square_rect.collidepoint(event.pos):
                                    actives[i] = [False, False, False]
                                    actives[i][j] = True
                                    if i == 0:
                                        players = 1
                                    elif i == 1:
                                        enemies = j
                                    else:
                                        size = map_sizes[j]
    
        # Clear the screen
        window.fill((100,100,100))
    
        # Draw main title
        window.blit(title_text, title_rect)
    
        # Draw back button
        pygame.draw.rect(window, (255, 0, 0), back_button_rect)
        back_button_rect_text = back_button_text.get_rect(center=back_button_rect.center)
        window.blit(back_button_text, back_button_rect_text)
    
        # Draw rows and columns
        for i, row_label_text in enumerate(row_label_texts):
            row_y = height // 4 + i * (height // 5)
    
            # Draw row label
            row_label_rect = row_label_text.get_rect(center=(width // 2, row_y - row_label_text.get_height()))
            window.blit(row_label_text, row_label_rect)
    
            for j, square_rect in enumerate(squares[i]):
                if actives[i][j]:
                    pygame.draw.rect(window, black, square_rect)
                else:
                    pygame.draw.rect(window, white, square_rect)
                if i == 0:
                    if actives[i][j]:
                        square_text = font_labels[i].render(str(1), True, white)
                    else:
                        square_text = font_labels[i].render(str(1), True, black)
                elif i == 1:
                    if actives[i][j]:
                        square_text = font_labels[i].render(str(j), True, white)
                    else:
                        square_text = font_labels[i].render(str(j), True, black)
                else:
                    if actives[i][j]:
                        square_text = font_labels[i].render(str(map_sizes[j]), True, white)
                    else:
                        square_text = font_labels[i].render(str(map_sizes[j]), True, black)
                square_text_rect = square_text.get_rect(center=square_rect.center)
                window.blit(square_text, square_text_rect)
    
        # Draw button
        pygame.draw.rect(window, (0, 255, 0), button_rect)
        button_rect_text = button_text.get_rect(center=button_rect.center)
        window.blit(button_text, button_rect_text)
    
        # Update the display
        pygame.display.flip()
    return [startGame, players, enemies, size]