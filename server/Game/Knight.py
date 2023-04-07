# Knight as child of Piece

from Game.Piece import Piece

class Knight(Piece):

    def __init__(self, x, y, owner, chessboard):
        super().__init__(x, y, owner, chessboard)
        self.point = 3

    

    def getMove(self):
        self.legalMoves = []
        tempMove = []
        #8 Possible L move
        possibleMovement = [[2,1], [2,-1], [1,2], [-1, 2], [-2,1], [-2,-1], [1,-2], [-1,-2]]
        chessboardTemp = self.chessboard.pieces

        for move in possibleMovement:
            if(self.isInsideBoard(self.x+move[0], self.y+move[1])):
                tempMove = [self.x+move[0], self.y+move[1]]
                self.legalMoves.append(tempMove)
        return self.samePieceOwnerCheck(self.legalMoves)


    def __str__(self) -> str:
        return "h"