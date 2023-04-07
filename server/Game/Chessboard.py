'''
Chessboard class
'''

import random
from typing import List

from Game.Piece import Piece
from Game.Player import Player
from Game.Pawn import Pawn
from Game.King import King
from Game.Rook import Rook
from Game.Knight import Knight
from Game.Bishop import Bishop
from Game.Queen import Queen
from Game.Star import Star


class Chessboard:
    size: int = 0

    def __init__(self, size):
        self.pieces = []
        self.size = size
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(None)
            self.pieces.append(temp)

    def addPiece(self, piece) -> bool:
        # If not empty
        if self.pieces[piece.x][piece.y] != None:
            return False

        self.pieces[piece.x][piece.y] = piece

        return True

    '''
    Add player pawn
    '''
    def addPlayerPawn(self, player, x: int, y: int):
        pawn = Pawn(x, y, player, self)
        return self.addPiece(pawn)

    '''
    Get piece movement

    Parameter:
    - x (int): piece x position
    - y (int): piece y position

    Return:
    - List of piece movement (List of [x, y]). For example, [[1,2],[2,3]]
    '''
    def getPieceMove(self, x: int, y: int):
        # If piece does not exist
        if self.pieces[x][y] == None:
            return []
        return self.pieces[x][y].getMove()

    # Function to move piece in chessboard
    def movePiece(self, piece, x: int, y:int) -> bool:
        oldTargetPiece = None
        # Cache the piece of target movement
        if x in range(8) and y in range(8):
            oldTargetPiece = self.pieces[x][y]
        # If the piece is moved successfully
        if piece.movePiece(x, y):
            #If we ate a king, commence the killPieces
            if oldTargetPiece != None:
                if oldTargetPiece.__str__() == "k":
                    #Set the player as not alive
                    oldTargetPiece.owner.isAlive = False
                    #Kill the remaining troops
                    self.killPieces(oldTargetPiece.getOwner())
            return True
        else:
            return False

    # Function to prepare chessboard
    # Initialize 3 pawns and a king for each player
    def prepare(self, players: List) -> bool:
        # Top
        if players[0]:
            player0 = players[0]
            # Creating pawns
            pawn0 = Pawn(0, 2, player0, self)
            pawn1 = Pawn(0, 4, player0, self)
            pawn2 = Pawn(1, 3, player0, self)
            # Creating king
            king = King(0, 3, player0, self)

            self.addPiece(pawn0)
            self.addPiece(pawn1)
            self.addPiece(pawn2)
            self.addPiece(king)

            pawn0.setOwner(player0)
            pawn1.setOwner(player0)
            pawn2.setOwner(player0)
            king.setOwner(player0)

            player0.position = 3

        # Bottom
        if players[1]:
            player1 = players[1]
            # Creating pawns
            pawn0 = Pawn(7, 2, player1, self)
            pawn1 = Pawn(7, 4, player1, self)
            pawn2 = Pawn(6, 3, player1, self)
            # Creating king
            king = King(7, 3, player1, self)

            self.addPiece(pawn0)
            self.addPiece(pawn1)
            self.addPiece(pawn2)
            self.addPiece(king)

            pawn0.setOwner(player1)
            pawn1.setOwner(player1)
            pawn2.setOwner(player1)
            king.setOwner(player1)

            player1.position = 1

        # Left
        if len(players) >= 3:
            player2 = players[2]
            # Creating pawns
            pawn0 = Pawn(2, 0, player2, self)
            pawn1 = Pawn(3, 1, player2, self)
            pawn2 = Pawn(4, 0, player2, self)
            # Creating king
            king = King(3, 0, player2, self)

            self.addPiece(pawn0)
            self.addPiece(pawn1)
            self.addPiece(pawn2)
            self.addPiece(king)

            pawn0.setOwner(player2)
            pawn1.setOwner(player2)
            pawn2.setOwner(player2)
            king.setOwner(player2)

            player2.position = 0

        # Right
        if len(players) >= 4:
            player3 = players[3]
            # Creating pawns
            pawn0 = Pawn(2, 7, player3, self)
            pawn1 = Pawn(3, 6, player3, self)
            pawn2 = Pawn(4, 7, player3, self)
            # Creating king
            king = King(3, 7, player3, self)

            self.addPiece(pawn0)
            self.addPiece(pawn1)
            self.addPiece(pawn2)
            self.addPiece(king)

            pawn0.setOwner(player3)
            pawn1.setOwner(player3)
            pawn2.setOwner(player3)
            king.setOwner(player3)

            player3.position = 2
        
        # Add random star
        countStar = 8
        while countStar > 0:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            if not self.pieces[x][y]:
                star = Star(x, y, self)
                self.addPiece(star)
                countStar -= 1
        return True

    # Procedure to print chessboard state for testing
    def print(self):
        for row in range(self.size):
            for col in range(self.size):
                piece = self.pieces[row][col]
                if piece:
                    print(str(piece) + " ", end="")
                else:
                    print("N ", end="")
            print("")
    
    '''
    Get chessboard state

    Return:
    - Array 2D representing chessboard state
    '''
    def getState(self):
        currState = []
        for row in range(self.size):
            rowState = []
            for col in range(self.size):
                piece = self.pieces[row][col]
                if piece:
                    rowState.append(str(piece))
                else:
                    rowState.append("--")
            currState.append(rowState)
        return currState
    
    '''
    Get chessboard owner state
    
    Return:
    - Array 2D containing owner name on each (x, y)
    '''
    def getOwnerState(self):
        currState = []
        for row in range(self.size):
            rowState = []
            for col in range(self.size):
                piece = self.pieces[row][col]
                if piece and piece.getOwner():
                    rowState.append(str(piece.getOwner().name))
                else:
                    rowState.append(None)
            currState.append(rowState)
        return currState

    
    # Function to promote a piece in the board
    def promotePiece(self, piece : Piece, pieceType):
        #Only pawn can be promoted
        if piece.__str__() != "p" :
            return False
        else:
            #Make the position empty then add new piece
            tempX = piece.x
            tempY = piece.y
            tempOwner = piece.owner
            self.pieces[piece.x][piece.y] = None
            '''
            Piece type is a string containing the type of piece
            That you want, i.e
            q = queen
            h = horse / knight
            c = castle / rook
            m = bishop
            '''
            if pieceType == "m" :
                bishop = Bishop(tempX, tempY, tempOwner, self)
                self.addPiece(bishop)
            elif pieceType == "h" :
                knight = Knight(tempX, tempY, tempOwner, self)
                self.addPiece(knight)
            elif pieceType == "c" :
                rook = Rook(tempX, tempY, tempOwner, self)
                self.addPiece(rook)
            elif pieceType == "q" :
                queen = Queen(tempX, tempY, tempOwner, self)
                self.addPiece(queen)
            return True
        return False

    '''
    Function to show owned pawn by a certain player
    Returns a list of pawn
    '''
    def getOwnPawns(self, player : Player):
        pawnPlace = []
        #Loop through the board to search for pawns
        for i in range(self.size):
            for j in range(self.size):
                if self.pieces[i][j] != None:
                    if self.pieces[i][j].getOwner() == player and self.pieces[i][j].__str__() == "p":
                        tempPiece = self.pieces[i][j]
                        pawnPlace.append(tempPiece)
        return pawnPlace
    
    '''
    Function get the coordinates of own pawn
    Returns a list of pawn's coordinates
    '''
    def getOwnPawnsCoordinates(self, pieces : Piece):
        tempCoordinates = []
        for pawn in pieces:
            tempXY = [pawn.x, pawn.y]
            tempCoordinates.append(tempXY)
        return tempCoordinates
    
    # Function to fuse several pawns into another pieces
    def fusionPiece(self, pieces, pieceType, x, y):
        # If target box is not empty
        if self.pieces[x][y] != None:
            return False
        tempStar = 0 #To count the value of the pawns
        fusionPossible = False #To know whether fusion is possible
        tempOwner = pieces[0].owner
        for piece in pieces:
            #We can only fuse pawns
            if piece.__str__() != "p":
                return False
            else:
                tempStar+=1
        '''
        Piece type is a string containing the type of piece
        That you want, i.e
        q = queen
        h = horse / knight
        c = castle / rook
        m = bishop
        '''
        if pieceType == "q" and tempStar >= 8:
            fusionPossible = True
        elif pieceType == "h" and tempStar >= 3:
            fusionPossible = True
        elif pieceType == "m" and tempStar >= 3:
            fusionPossible = True
        elif pieceType == "r" and tempStar >= 5:
            fusionPossible = True
        #Delete all pawns and replace it with new piece
        if fusionPossible == True:
            for piece in pieces:
                #Delete the piece
                self.pieces[piece.x][piece.y] = None
            #Add new piece
            if pieceType == "m" :
                bishop = Bishop(x, y, tempOwner, self)
                self.addPiece(bishop)
            elif pieceType == "h" :
                knight = Knight(x, y, tempOwner, self)
                self.addPiece(knight)
            elif pieceType == "c" :
                rook = Rook(x, y, tempOwner, self)
                self.addPiece(rook)
            elif pieceType == "q" :
                queen = Queen(x, y, tempOwner, self)
                self.addPiece(queen)
            return True
        else: return False

    '''
    Function to kill remaining pieces of a player if
    that player is no longer alive
    '''
    def killPieces(self, player : Player):
        for i in range(self.size):
            for j in range(self.size):
                if self.pieces[i][j] != None:
                    if self.pieces[i][j].getOwner() and self.pieces[i][j].getOwner() == player:
                        self.pieces[i][j] = None