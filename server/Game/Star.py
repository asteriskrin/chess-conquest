# Star as child of Piece

from Game.Piece import Piece

class Star(Piece):

    def __init__(self, x, y, chessboard):
        super().__init__(x, y, None, chessboard)
        self.point = 5

    
    def move(self, x, y):
        return False

    def getMove(self):
        return []

    def __str__(self) -> str:
        return "star"