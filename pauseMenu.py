import sys
import pygame
from font import getNoneFont


def pauseMenu(screen, width, height):
    paused = True
    end = False
    while paused:                    
        # Define the rectangle dimensions
        menu_width, menu_height = width//2, height/1.2*0.8
        
        # Calculate the position of the top-left corner of the rectangle
        menu_x = (width - menu_width) // 2
        menu_y = (height/1.2 - menu_height) // 2
        
        # Draw the rectangle
        pygame.draw.rect(screen, (120, 120, 120), (menu_x, menu_y, menu_width, menu_height))

        # Render and draw text at the top
        font = getNoneFont("Pause Menu", menu_width*0.7, menu_height*0.7)
        text = font.render("Pause Menu", True, (0,0,0))
        text_rect = text.get_rect(center=(width // 2, menu_y * 2))
        screen.blit(text, text_rect)

        # Define button dimensions
        button_width, button_height = menu_width * 0.7, menu_height * 0.1

        # Calculate button positions
        button1_x = (menu_width - button_width) / 2 + menu_x
        button1_y = menu_height / 3 + menu_y

        #button2_x = (width - button_width) // 2
        #button2_y = button1_y + button_height + 20

        button3_x = (menu_width - button_width) / 2 + menu_x
        button3_y = button1_y + button_height * 1.5

        # Draw buttons
        pygame.draw.rect(screen, (0, 255, 0), (button1_x, button1_y, button_width, button_height))
        #pygame.draw.rect(screen, (0, 0, 255), (button2_x, button2_y, button_width, button_height))
        pygame.draw.rect(screen, (255, 0, 0), (button3_x, button3_y, button_width, button_height))

        # Render and draw text on buttons
        button1_font = getNoneFont("Continue", button_width*0.8, button_height*0.8)
        button1_text = button1_font.render("Continue", True, (0,0,0))
        #button2_text = button_font.render("Settings", True, (0,0,0))
        button3_font = getNoneFont("Main Menu", button_width*0.8, button_height*0.8)
        button3_text = button3_font.render("Main Menu", True, (0,0,0))

        screen.blit(button1_text, button1_text.get_rect(center=(button1_x + button_width // 2, button1_y + button_height // 2)))
        #screen.blit(button2_text, (button2_x + 10, button2_y + 10))
        screen.blit(button3_text, button3_text.get_rect(center=(button3_x + button_width // 2, button3_y + button_height // 2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if mouse click is within the boundaries of the buttons
                if (
                    button1_x <= mouse_x <= button1_x + button_width
                    and button1_y <= mouse_y <= button1_y + button_height
                ):
                    paused = False
                elif (
                    button3_x <= mouse_x <= button3_x + button_width
                    and button3_y <= mouse_y <= button3_y + button_height
                ):
                    paused = False
                    end = True

        # Update the display
        pygame.display.flip()
    return end