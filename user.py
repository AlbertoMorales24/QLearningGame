class User:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.orientation = "right"
        self.vidas = 15
        self.puntos = 0
        self.puntos2 = 0
    
    def getX(self, g_size):
        return self.col * g_size + g_size // 2