'''
Chessboard Section class
'''

import pygame
from frontend.ChessboardAsset import ChessboardAsset

class ChessboardSection:
    COLOR_DARK_BLUE = pygame.Color("dark red")
    asset = None

    def __init__(self, sqSize, dimension):
        self.sqSize = sqSize
        self.dimension = dimension
        self.highlight = []
        self.asset = ChessboardAsset(sqSize)

    def drawGameState(self, screen, chessboardState, ownerState):
        self.__drawBoard(screen)
        self.__drawPieces(chessboardState, screen)

    def __drawBoard(self, screen):
        colors = [pygame.Color("white"), pygame.Color("gray")]

        for r in range(self.dimension):
            for c in range(self.dimension):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(c * self.sqSize + 80, r * self.sqSize + 80, self.sqSize, self.sqSize))

    def drawHighlight(self, screen):
        for coord in self.highlight:
            r = coord[0]
            c = coord[1]
            pygame.draw.rect(screen, self.COLOR_DARK_BLUE, pygame.Rect(c * self.sqSize + 80 + 30, r * self.sqSize + 80 + 30, 10, 10))

    def __drawPieces(self, chessboardState, screen):
        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = chessboardState[r][c]
                if piece != "--":
                    screen.blit(self.asset.IMAGES[piece], pygame.Rect(c * self.sqSize + 80, r * self.sqSize + 80, self.sqSize, self.sqSize))

    def addHighlight(self, row, col):
        self.highlight.append([row, col])

    def removeHighlight(self):
        self.highlight.clear()
        
