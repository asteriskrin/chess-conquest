# Knight as child of Piece

from Game.Piece import Piece

class Bishop(Piece):

    def __init__(self, x, y, owner, chessboard):
        super().__init__(x, y, owner, chessboard)
        self.point = 3

    

    def getMove(self):
        self.legalMoves = []
        tempMove = []
        tempChessboard = self.chessboard.pieces
        possibleMoves = [[-1,-1], [-1,1], [1,-1], [1,1]]
        #Diagonal Moves, 4 diagonals
        #Left-Up, Right-Up, Left-Down, Right-Down
        tempX = self.x
        tempY = self.y
        for move in possibleMoves:
            tempX = self.x
            tempY = self.y
            while(self.isInsideBoard(tempX+move[0], tempY+move[1])):
                tempX += move[0]
                tempY += move[1]
                tempMove = [tempX, tempY]
                self.legalMoves.append(tempMove)
                if tempChessboard[tempX][tempY] != None:
                    break
        
        return self.samePieceOwnerCheck(self.legalMoves)


    def __str__(self) -> str:
        return "m"