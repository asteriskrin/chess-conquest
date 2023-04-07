# Pawn as child of Piece

from Game.Piece import Piece


class Pawn(Piece):
    # Orientation of pawn to determine pawn's movement
    # Get orientation from Player class

    def __init__(self, x, y, owner, chessboard):
        super().__init__(x, y, owner, chessboard)
        self.point = 1
 

    #Position determines the type of movement
    #0 = Left to right
    #1 = Bottom to top
    #2 = Right to left
    #3 = Up to down
    #Also checks for avaiable piece to "eat"
    def getMove(self):
        self.legalMoves = []
        tempMove = []
        tempChessboard = self.chessboard.pieces
        position = self.owner.position
        if position == 0:
            #print("It is position 0")
            #print(self.legalMoves)
            if self.y+1 < self.chessboard.size :
                #Forward movement
                if tempChessboard[self.x][self.y+1] == None: 
                    tempMove = [self.x, self.y+1]
                    self.legalMoves.append(tempMove)
                #Eat the diagonal pieces
                if self.x-1 >= 0 :
                    if tempChessboard[self.x-1][self.y+1] != None: 
                        tempMove = [self.x-1, self.y+1]
                        self.legalMoves.append(tempMove)
                if self.x+1 < self.chessboard.size :
                    if tempChessboard[self.x+1][self.y+1] != None: 
                        tempMove = [self.x+1, self.y+1]
                        self.legalMoves.append(tempMove)
        elif position == 1:
            if self.x-1 < self.chessboard.size :
                #Forward movement
                if tempChessboard[self.x-1][self.y] == None: 
                    tempMove = [self.x-1, self.y]
                    self.legalMoves.append(tempMove)
                #Eat the diagonal pieces
                if self.y-1 >= 0 :
                    if tempChessboard[self.x-1][self.y-1] != None: 
                        tempMove = [self.x-1, self.y-1]
                        self.legalMoves.append(tempMove)
                if self.y+1 < self.chessboard.size :
                    if tempChessboard[self.x-1][self.y+1] != None: 
                        tempMove = [self.x-1, self.y+1]
                        self.legalMoves.append(tempMove)
        elif position == 2:
            if self.y-1 < self.chessboard.size :
                #Forward movement
                if tempChessboard[self.x][self.y-1] == None: 
                    tempMove = [self.x, self.y-1]
                    self.legalMoves.append(tempMove)
                #Eat the diagonal pieces
                if self.x-1 >= 0 :
                    if tempChessboard[self.x-1][self.y-1] != None: 
                        tempMove = [self.x-1, self.y-1]
                        self.legalMoves.append(tempMove)
                if self.x+1 < self.chessboard.size :
                    if tempChessboard[self.x+1][self.y-1] != None: 
                        tempMove = [self.x+1, self.y-1]
                        self.legalMoves.append(tempMove)
        elif position == 3:
            if self.x+1 < self.chessboard.size :
                #Forward movement
                if tempChessboard[self.x+1][self.y] == None: 
                    tempMove = [self.x+1, self.y]
                    self.legalMoves.append(tempMove)
                #Eat the diagonal pieces
                if self.y-1 >= 0 :
                    if tempChessboard[self.x+1][self.y-1] != None: 
                        tempMove = [self.x+1, self.y-1]
                        self.legalMoves.append(tempMove)
                if self.y+1 < self.chessboard.size :
                    if tempChessboard[self.x+1][self.y+1] != None: 
                        tempMove = [self.x+1, self.y+1]
                        self.legalMoves.append(tempMove)
        return self.samePieceOwnerCheck(self.legalMoves)

    def __str__(self) -> str:
        return "p"
