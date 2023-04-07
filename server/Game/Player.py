'''
Player class
'''

import string
from typing import List
#from Game.Piece import Piece

class Player:
    socketId: int = None
    name: string = None
    star: int = 0
    pieces: List = None
    time: int = 0
    position: int = 0
    room = None
    isAlive : bool = True

    @staticmethod
    def createPlayer(socketId: int, name: string):
        player = Player()
        player.socketId = socketId
        player.name = name
        return player
    
    def movePiece(self, piece, x: int, y: int) -> bool:
        # If player is not in any rooms
        if not self.room:
            return False
        
        # If player tries to move piece that he does not own
        # if piece not in self.pieces:
            # return False

        return self.room.movePiece(self, piece, x, y)

    '''
    Player promote pawn
    '''
    def promotePawn(self, x, y, pieceType):
        price = Player.__getPiecePrice(pieceType)
        if self.star < price:
            return False
        if self.room.promotePawn(self, x, y, pieceType):
            self.star -= price
            return True
        return False

    '''
    Player fusion piece
    '''
    def fusionPiece(self, pieceType, x, y):
        return self.room.fusionPiece(self, pieceType, x, y)

    '''
    Player buy pawn
    '''
    def buyPawn(self, x: int, y: int):
        price = 1
        if self.star < price:
            return False
        if self.room.playerBuyPawn(self, x, y):
            self.star -= price
            return True
        return False

    @staticmethod
    def __getPiecePrice(pieceType):
        if pieceType == "h" or pieceType == "m":
            return 3
        elif pieceType == "c":
            return 5
        elif pieceType == "q":
            return 8
        return 0

    '''
    Has room
    '''
    def hasRoom(self) -> bool:
        if self.room: return True
        return False

    '''
    Get room
    '''
    def getRoom(self):
        return self.room
