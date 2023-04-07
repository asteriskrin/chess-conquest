# Piece class

from Game.Player import Player
# from Game.Chessboard import Chessboard

class Piece:
    # Variables, x & y is position on board
    # x is vertical
    # y is horizontal
    # (0,0) is top left of board
    x : int = int(0)
    y : int = int(0)
    owner : Player = None
    chessboard = None
    legalMoves = [] #To store legal / possible moves without considering "eating"
    point : int = int(0) #The amount of point or value of a piece

    def __init__(self, x, y, owner, chessboard):
        self.x = x
        self.y = y
        self.owner = owner
        self.chessboard = chessboard
    
    #Function to check if a move is within reach / range
    def move(self, x, y):
        self.getMove()
        newPosition = [x,y]
        if newPosition in self.legalMoves:
            return True
        return False

    #Function to get available moves
    def getMove(self):
        return []

    #To return a representation of piece in string
    def __str__(self) -> str:
        return "--"
    
    #To know whether a piece is inside the board
    def isInsideBoard(self, x, y):
        if x >= 0 and x < self.chessboard.size and y >= 0 and y < self.chessboard.size :
            return True
        return False

    #To move and possibly "eat" other piece
    def movePiece(self, x, y):
        if(self.move(x, y) == True):
            #Check whether x,y contains another piece
            if self.chessboard.pieces[x][y] == None:
                self.chessboard.pieces[x][y] = self # Move the piece
                self.chessboard.pieces[self.x][self.y] = None # Make the original position empty
                self.x = x
                self.y = y
                return True
            elif self.chessboard.pieces[x][y] != None:
                #If the piece is not owned by the same player
                if self.chessboard.pieces[x][y].getOwner() != self.getOwner():
                    self.owner.star += self.chessboard.pieces[x][y].point
                    self.chessboard.pieces[x][y] = self
                    self.chessboard.pieces[self.x][self.y] = None
                    self.x = x
                    self.y = y
                    return True
                elif self.chessboard.pieces[x][y].getOwner() == self.getOwner():
                    return False
        return False

    #Get the owner of a piece
    def getOwner(self):
        return self.owner

    #Set piece owner
    def setOwner(self, player):
        self.owner = player
    
    #To check and eliminate attacking own piece in legal moves 
    def samePieceOwnerCheck(self, rawLegalMoves):
        tempLegalMoves = []
        self.legalMoves = rawLegalMoves
        for move in self.legalMoves:
            if self.chessboard.pieces[move[0]][move[1]] == None:
                tempLegalMoves.append(move)
            else: 
                if self.chessboard.pieces[move[0]][move[1]].getOwner() != self.getOwner():
                    tempLegalMoves.append(move)
        self.legalMoves = tempLegalMoves
        return self.legalMoves
