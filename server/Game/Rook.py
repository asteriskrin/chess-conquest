# Rook as child of Piece

from Game.Piece import Piece
from array import *

class Rook(Piece):

    def __init__(self, x, y, owner, chessboard):
        super().__init__(x, y, owner, chessboard)
        self.point = 5

    

    #To get the available moves        
    def getMove(self):
        self.legalMoves = []
        chessboardTemp = self.chessboard.pieces #To store pieces location in chessboard
        #|n|n|n|n|n|
        #|n|n|n|r|n|
        #|n|n|n|n|n|

        #legalMoves = [] #To store legal / available moves
        
        #To specify boundaries
        leftY   = 0
        rightY  = self.chessboard.size
        upX     = 0
        downX   = self.chessboard.size

        #4 directional expansion of legal move
        #Up, down, right, left
        for i in range(self.x-1, upX-1, -1):
            tempPair = [i, self.y]
            self.legalMoves.append(tempPair)
            if chessboardTemp[i][self.y] != None:
                break
        for i in range(self.x+1, downX):
            tempPair = [i, self.y]
            self.legalMoves.append(tempPair)
            if chessboardTemp[i][self.y] != None:
                break
        for j in range(self.y+1, rightY):
            tempPair = [self.x, j]
            self.legalMoves.append(tempPair)
            if chessboardTemp[self.x][j] != None:
                break
        for j in range(self.y-1, leftY-1, -1):
            tempPair = [self.x, j]
            self.legalMoves.append(tempPair)
            if chessboardTemp[self.x][j] != None:
                break
        
        
        return self.samePieceOwnerCheck(self.legalMoves)

    def __str__(self) -> str:
        return "c"