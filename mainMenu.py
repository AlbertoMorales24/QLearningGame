import random
import sys
import pygame

from button import Button
from credits import showCredits
from font import getFont
from instructions import showInstructions
from finalGame import game
from settings import settings
from gameSettings import setGame

def startMainMenu():
    mainMenuRunning = True
    screenWidth = settings['screenWidth']
    screenHeight = settings['screenHeight']
    minSize = min(screenHeight, screenWidth)
    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("PAC-MANIA")
    BG = pygame.image.load("assets/Background.png")
    BG = pygame.transform.scale(BG, (screenWidth, screenHeight))
    seed = settings['seed']
    while mainMenuRunning:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = getFont("PAC-MANIA", minSize*0.7, minSize*0.7).render("PAC-MANIA", True, settings['menuTitleColor'])
        menuTextCenter = (screenWidth // 2, screenHeight * 0.2)
        MENU_RECT = MENU_TEXT.get_rect(center=menuTextCenter)

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(screenWidth // 2, screenHeight * 0.4), 
                            textInput="PLAY", font=getFont("PAC-MANIA", minSize*0.5, minSize*0.5), base_color="#d7fcd4", hovering_color="Green")
        INSTRUCTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(screenWidth // 2, screenHeight * 0.6), 
                            textInput="HOW TO PLAY", font=getFont("PAC-MANIA", minSize*0.5, minSize*0.5), base_color="#d7fcd4", hovering_color="Yellow")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(screenWidth // 2, screenHeight * 0.8), 
                            textInput="QUIT", font=getFont("PAC-MANIA", minSize*0.5, minSize*0.5), base_color="#d7fcd4", hovering_color="Red")
        CREDITS_BUTTON = Button(image=None, pos=(screenWidth // 8, screenHeight * 0.95), 
                            textInput="CREDITS", font=getFont("PAC-MANIA", minSize*0.3, minSize*0.3), base_color="#d7fcd4", hovering_color="Gray")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, INSTRUCTIONS_BUTTON, QUIT_BUTTON, CREDITS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_settings = setGame()
                    if game_settings[0]:
                        game(seed, game_settings[1], game_settings[2], game_settings[3])
                        ## Return Screen to size for main menu
                    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
                if INSTRUCTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    showInstructions()
                    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    showCredits()
                    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    mainMenuRunning = False
                    break
        if mainMenuRunning:
            pygame.display.update()

def playMusic(track):
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)
   
pygame.init()
##playMusic("./assets/musicMenu.mp3")
startMainMenu()