import pygame


def getFont(text, maxWidth, maxHeight): # Returns Press-Start-2P in the desired size
    fontPath = "assets/font.ttf"
    size = calculateFontSize(text, maxWidth, maxHeight, fontPath)
    return pygame.font.Font(fontPath, size)

def getNoneFont(text, maxWidth, maxHeight): # Returns Press-Start-2P in the desired size
    fontPath = "assets/font.ttf"
    size = calculateFontSize(text, maxWidth, maxHeight, fontPath)
    return pygame.font.Font(fontPath, size)

def calculateFontSize(text, maxWidth, maxHeight, fontPath):
    """
    Calculates the optimal font size for a given text to fit within specified width and height.

    Parameters:
    - text (str): The text to be rendered.
    - max_width (int): The maximum allowable width for the text.
    - max_height (int): The maximum allowable height for the text.
    - font_path (str): The path to the font file. Defaults to 'freesansbold.ttf'.

    Returns:
    - int: The calculated font size.
    """
    font_size = 1  # Start with a small font size
    font = pygame.font.Font(fontPath, font_size)

    # Get the size of the rendered text
    text_size = font.size(text)

    # Increase font size until the text exceeds the maximum dimensions
    while text_size[0] <= maxWidth and text_size[1] <= maxHeight:
        font_size += 1
        font = pygame.font.Font(fontPath, font_size)
        text_size = font.size(text)

    # Return the last valid font size that fits within the dimensions
    return font_size - 1  # Return the previous size before exceeding limits