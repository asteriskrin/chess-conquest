'''
Room class
'''

import random
import string
import logging
from typing import List
from Game.Chessboard import Chessboard
from Game.Player import Player

class Room:
    roomId: int = 0
    host: Player = None
    players: List[Player] = []
    chessboard: Chessboard = None
    start: bool = False
    turn = 0

    def __init__(self, roomId: int, host: Player, chessboard: Chessboard):
        self.roomId = roomId
        self.host = host
        self.chessboard = chessboard
        # Reset player
        self.players = []
        self.players.append(host)
        self.host.room = self
        self.start = False

    def joinPlayer(self, player: Player) -> bool:
        if len(self.players) < 4:
            self.players.append(player)
            player.room = self
            return True
        else:
            return False

    def start(self) -> bool:
        # If the match is started already
        if self.start:
            return False
        self.start = True
        return True

    '''
    Count player in room
    '''
    def countPlayer(self):
        return len(self.players)

    '''
    Count alive player
    '''
    def countAlivePlayer(self):
        c = 0
        for p in self.getPlayers():
            if p.isAlive:
                c += 1
        return c
    
    def kickPlayer(self, player: Player):
        # Turn check
        wasHisTurn = False
        if self.getTurnPlayer() == player:
            wasHisTurn = True
        # Remove player from list
        self.players.remove(player)
        # Turn check
        if wasHisTurn:
            if self.turn >= len(self.players) or not self.getTurnPlayer().isAlive:
                self.nextTurn()
        # If the player is host, give host privilege to someone else
        if self.host == player and len(self.players) > 0:
            # Give host privilege to random people in room
            self.host = random.choice(self.players)
        self.chessboard.killPieces(player)

    def isHost(self, player: Player) -> bool:
        if player == self.host:
            return True
        else:
            return False
    
    def getTurnPlayer(self):
        if self.turn >= len(self.players): return None
        index = self.turn
        return self.players[index]

    '''
    To get next turn
    also to check whether there is a skipped turn and winner
    return False means the game is still ongoing, True means it has
    ended
    '''
    def nextTurn(self):
        if len(self.players) == 0:
            self.turn = 0
            return False
        originalTurn = self.turn
        # Loop until found winner or there is a valid turn
        while True :
            # Increment turn
            self.turn += 1
            # Circular turn
            if self.turn >= len(self.players):
                self.turn = 0
            # Check whether the player is alive or not
            if self.getTurnPlayer().isAlive == False:
                continue
            else:
                break
        if self.turn == originalTurn:
            return True


    def movePiece(self, player, piece, x: int, y: int) -> bool:
        # If it is not the player's turn
        if self.getTurnPlayer() != player:
            return False

        # Move the piece
        if self.chessboard.movePiece(piece, x, y):
            # Give turn to the next player
            self.nextTurn()
            return True
        return False

    '''
    Promote piece
    '''
    def promotePawn(self, player, x, y, pieceType):
        if self.getTurnPlayer() != player:
            return False
        piece = self.chessboard.pieces[x][y]
        if self.chessboard.promotePiece(piece, pieceType):
            # Give turn to the next player
            self.nextTurn()
            return True
        return False

    '''
    Fusion piece
    '''
    def fusionPiece(self, owner, pieceType: string, x: int, y: int):
        pieces = []
        for row in range(0, self.chessboard.size):
            for col in range(0, self.chessboard.size):
                if self.chessboard.pieces[row][col] and str(self.chessboard.pieces[row][col]) == 'p' and self.chessboard.pieces[row][col].getOwner() and self.chessboard.pieces[row][col].getOwner() == owner:
                    pieces.append(self.chessboard.pieces[row][col])

        if self.chessboard.fusionPiece(pieces, pieceType, x, y):
            self.nextTurn()
            return True
        return False

    '''
    Player buy pawn
    '''
    def playerBuyPawn(self, player, x: int, y: int):
        if self.chessboard.addPlayerPawn(player, x, y):
            self.nextTurn()
            return True
        return False

    '''
    Get player star data
    '''
    def getPlayerStarData(self):
        data = []
        for p in self.players:
            data.append([p.name, p.star])
        return data

    '''
    Get list of players in the room
    '''
    def getPlayers(self):
        if self.players: return self.players
        return []

    '''
    Get player by index
    '''
    def getPlayer(self, index: int):
        try:
            return self.players[index]
        except:
            logging.error("List of player is undefined")
        return None

    # Function to start game
    def startGame(self) -> bool:
        # If there is less than 2 players in the room
        if len(self.players) < 2:
            return False

        # Prepare chessboard (initialize pawn and king for each player)
        if self.chessboard.prepare(self.players):
            self.start = True
            return True
        else:
            return False

    '''
    Get player by name
    '''
    def getPlayerByName(self, playerName: string):
        for p in self.getPlayers():
            if p.name == playerName:
                return p
        return None

    '''
    Destroy room
    '''
    def destroy(self):
        # Destroy chessboard
        self.chessboard.destroy()
        
