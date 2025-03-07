import pygame
from font import getNoneFont

def loadingScreen(screen, width, height):
    screen.fill((65,172,57))
    # Choose a font and size
    font = getNoneFont("Loading Map...", width*0.8, height*0.8)
    
    # Create a text surface
    text = font.render("Loading Map...", True, (0,0,0))
    
    # Get the rect of the text surface
    text_rect = text.get_rect(center=(width // 2, height // 2))

    # Blit the text onto the screen
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()