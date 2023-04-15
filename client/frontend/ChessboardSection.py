'''
Chessboard Section class
'''

import pygame
import math
from frontend.ChessboardAsset import ChessboardAsset

class ChessboardSection:
    COLOR_DARK_BLUE = pygame.Color("dark red")
    asset = None

    def __init__(self, sqSize, dimension):
        self.sqSize = sqSize
        self.dimension = dimension
        self.highlight = []
        self.movingPiece = None
        self.indexAnim = 0
        self.asset = ChessboardAsset(sqSize)

    def setMovingPiece(self, movingPiece):
        self.movingPiece = movingPiece
        self.indexAnim = 0

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

    # TODO: Fix the formula so that r is not 0 and the formula returns the correct output
    # Formula to calculate the offset of translated piece to be animated
    def __calculateTranslatedPiece(self, sx, sy, fx, fy):
        dy = fy - sy
        dx = fx - sx
        r = math.hypot(dx, dy)
        if r == 0:
            r = 1
        
        sinVal = dy/r
        cosVal = dx/r

        newR = (15 - self.indexAnim) / 15 * r
        newX = cosVal*newR
        newY = sinVal*newR
        return newX, newY

    def __drawPieces(self, chessboardState, screen):
        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = chessboardState[r][c]
                if piece != "--":
                    # If this is the moving piece
                    if self.movingPiece:
                        print(f"c = {c} and r = {r} , self.movingPiece = {str(self.movingPiece)}")
                    if self.movingPiece and c == self.movingPiece[2] and r == self.movingPiece[3]:
                        # Render animated piece
                        transX, transY = self.__calculateTranslatedPiece(self.movingPiece[0], self.movingPiece[1],
                            self.movingPiece[2], self.movingPiece[3])
                        c_translated = c + transX
                        r_translated = r + transY
                        screen.blit(self.asset.IMAGES[piece], pygame.Rect(c_translated * self.sqSize + 80, r_translated * self.sqSize + 80, self.sqSize, self.sqSize))
                        
                        self.indexAnim += 1

                        if self.indexAnim == 16:
                            self.movingPiece = None
                            self.indexAnim = 0
                    else:
                        screen.blit(self.asset.IMAGES[piece], pygame.Rect(c * self.sqSize + 80, r * self.sqSize + 80, self.sqSize, self.sqSize))

    def addHighlight(self, row, col):
        self.highlight.append([row, col])

    def removeHighlight(self):
        self.highlight.clear()
        
