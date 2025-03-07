import sys
import pygame

from button import Button
from font import getFont
from settings import settings

import pygame
def resize_image(screen_width, screen_height, original_image):
    # Calculate maximum allowed dimensions (70% of screen size)
    max_width = 0.7 * screen_width
    max_height = 0.7 * screen_height

    # Calculate potential scaling factors for both dimensions
    width_scale = max_width / 3  # 3 is the width component of 3:4 ratio
    height_scale = max_height / 4  # 4 is the height component of 3:4 ratio

    # Use the smaller scale to ensure both dimensions fit within limits
    scale = min(width_scale, height_scale)

    # Calculate final dimensions while maintaining aspect ratio
    new_width = int(3 * scale)
    new_height = int(4 * scale)

    # Scale the image using smooth scaling
    return pygame.transform.smoothscale(original_image, (new_width, new_height))


def showInstructions():
    screenWidth = settings['screenWidth']
    screenHeight = settings['screenHeight']
    minSize = min(screenHeight, screenWidth)
    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("PAC-MANIA")
    instructionShown = True
    while instructionShown:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("#FF7F50")
        
        img = pygame.image.load("assets/Intruction.png")        
        OPTIONS_IMG = resize_image(screenWidth, screenHeight, img)  # Adjust the path as needed

        # Calculate the center position for the resized image
        img_width, img_height = OPTIONS_IMG.get_size()
        center_x = (screenWidth - img_width) // 2
        center_y = (screenHeight - img_height) // 2
        
        SCREEN.blit(OPTIONS_IMG, (center_x, center_y))

        OPTIONS_TEXT = getFont("HOW TO PLAY", minSize*0.6, minSize*0.6).render("HOW TO PLAY", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screenWidth*0.5, screenHeight*0.1))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(screenWidth*0.12, screenHeight*0.05), 
                            textInput="BACK", font=getFont("BACK", minSize*0.1, minSize*0.1), base_color="Black", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    instructionShown = False
                    break
        pygame.display.update()