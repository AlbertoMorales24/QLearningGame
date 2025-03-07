import sys
import pygame

from button import Button
from font import getFont
from settings import settings

def resize_image(screen_width, screen_height, original_image):
    # Get original image dimensions
    original_width, original_height = original_image.get_size()
    aspect_ratio = original_width / original_height

    # Calculate maximum allowed dimensions
    max_width = 0.5 * screen_width
    max_height = 0.3 * screen_height

    # Calculate scale factors for both dimensions
    width_scale = max_width / original_width
    height_scale = max_height / original_height

    # Use the most restrictive scale factor to maintain aspect ratio
    scale = min(width_scale, height_scale)

    # Calculate new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Only scale down if necessary, not up
    if scale < 1:
        return pygame.transform.smoothscale(original_image, (new_width, new_height))
    else:
        return original_image  # Return original if smaller than max dimensions

def showCredits():
    screenWidth = settings['screenWidth']
    screenHeight = settings['screenHeight']
    minSize = min(screenHeight, screenWidth)
    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
    creditsShowing = True
    while creditsShowing:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = getFont("CREDITS", minSize*0.5, minSize*0.5).render("CREDITS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screenWidth*0.5, screenHeight*0.2))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        img = pygame.image.load("assets/credits.png")
        CRED_IMG = resize_image(screenWidth, screenHeight, img)
        # Calculate the center position for the resized image
        img_width, img_height = CRED_IMG.get_size()
        center_x = (screenWidth - img_width) // 2
        center_y = (screenHeight - img_height) // 2
        
        SCREEN.blit(CRED_IMG, (center_x, center_y))

        OPTIONS_BACK = Button(image=None, pos=(screenWidth*0.1, screenHeight*0.05), 
                            textInput="BACK", font=getFont("BACK", minSize*0.1, minSize*0.1), base_color="Black", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN  and event.button == 1:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    creditsShowing = False
                    break

        pygame.display.update()