'''
GameController class
'''

import random
from socket import socket
import string
from typing import Dict, List
from Game.Chessboard import Chessboard
from Game.Player import Player
from Game.Room import Room


class GameController:
    socketPlayerMap: Dict = {}
    rooms: List[Room] = []
    
    def __init__(self):
        # Reset room
        self.rooms = []
        # Reset socket
        self.socketPlayerMap = {}

    '''
    Create room function
    '''
    def createRoom(self, socketId: int, playerName: string):
        player = self.makePlayer(socketId, playerName)
        room = self.makeRoom(player)
        if room:
            return room.roomId
        return -1

    '''
    Enter room function
    '''
    def enterRoom(self, socketId: int, playerName: string, roomId: int):
        player = self.makePlayer(socketId, playerName)
        if self.joinRoom(player, roomId):
            room = player.room
            data = self.__getPlayerSocketName(room)
            return room.roomId, data
        return -1, []

    '''
    Get piece movement
    '''
    def getPieceMove(self, roomId: int, x: int, y: int):
        room = self.__findRoomById(roomId)
        # If room does not exist
        if room == None:
            return []
        return room.chessboard.getPieceMove(x, y)

    '''
    Get turn player
    '''
    def getTurnPlayer(self, roomId: int):
        room = self.__findRoomById(roomId)
        # If room does not exist
        if room == None:
            return None
        return room.getTurnPlayer()

    '''
    Player move piece
    '''
    def playerMovePiece(self, playerSocketId: int, sx: int, sy: int, fx: int, fy: int):
        player = self.getPlayerBySocketId(playerSocketId)
        room = player.room
        # If room does not exist
        if room == None:
            return None, [None, None], None, None, None, None
        chessboard = room.chessboard
        piece = chessboard.pieces[sx][sy]
        # If piece does not exist
        if piece == None:
            return None, [None, None], None, None, None, None
        # If moving piece is successful
        if player.movePiece(piece, fx, fy):
            nextTurn = room.getTurnPlayer()
            # No other player to give turn to
            winner = None
            if nextTurn == player:
                winner = player.name
            return chessboard.getState(), [nextTurn.socketId, nextTurn.name], chessboard.getOwnerState(), self.__getPlayerSocketName(room), room.getPlayerStarData(), winner
        return None, [None, None], None, None, None, None

    '''
    Promote pawn
    '''
    def promotePawn(self, playerSocketId: int, x: int, y: int, pieceType: string):
        player = self.getPlayerBySocketId(playerSocketId)
        if player.promotePawn(x, y, pieceType):
            room = player.room
            chessboard = room.chessboard
            nextTurn = room.getTurnPlayer()
            return chessboard.getState(), [nextTurn.socketId, nextTurn.name], chessboard.getOwnerState(), self.__getPlayerSocketName(room), room.getPlayerStarData()
        return None, [None, None], None, None, None
    
    '''
    Fusion piece
    '''
    def fusionPiece(self, playerSocketId: int, pieceType: string, x: int, y: int):
        player = self.getPlayerBySocketId(playerSocketId)
        if player.fusionPiece(pieceType, x, y):
            room = player.room
            chessboard = room.chessboard
            nextTurn = room.getTurnPlayer()
            return chessboard.getState(), [nextTurn.socketId, nextTurn.name], chessboard.getOwnerState(), self.__getPlayerSocketName(room)
        return None, [None, None], None, None

    '''
    Buy pawn
    '''
    def buyPawn(self, playerSocketId: int, x: int, y: int):
        player = self.getPlayerBySocketId(playerSocketId)
        if player.buyPawn(x, y):
            room = player.room
            chessboard = room.chessboard
            nextTurn = room.getTurnPlayer()
            return chessboard.getState(), [nextTurn.socketId, nextTurn.name], chessboard.getOwnerState(), self.__getPlayerSocketName(room), room.getPlayerStarData()
        return None, [None, None], None, None, None

    '''
    Player disconnect
    '''
    def playerDisconnect(self, playerSocketId: int):
        player = self.getPlayerBySocketId(playerSocketId)
        winner = None
        newHost = None
        # If player socket ID is not found
        if not player: return False, {}
        if player.hasRoom():
            room = player.getRoom()
            room.kickPlayer(player)
            # If there is no player in the room
            if room.countAlivePlayer() == 0:
                return False, {}
            elif room.countAlivePlayer() == 1:
                if room.start:
                    winnerPlayer = room.getTurnPlayer()
                    winner = [winnerPlayer.socketId, winnerPlayer.name]
            if not room.start:
                newHost = room.host.name
            nextTurn = room.getTurnPlayer()
            return True, {
                "WINNER": winner, 
                "NEXT_TURN": [nextTurn.socketId, nextTurn.name], 
                "PLAYER_LIST": self.__getPlayerSocketName(room), 
                "STAR_DATA": room.getPlayerStarData(),
                "CHESSBOARD_STATE": room.chessboard.getState(),
                "OWNER_STATE": room.chessboard.getOwnerState(),
                "WHO_DISCONNECT": player.name,
                "NEW_HOST": newHost
            }
        return False, {}

    '''
    Kill player (for testing)
    '''
    def playerKill(self, playerSocketId: int):
        player = self.getPlayerBySocketId(playerSocketId)
        if not player: return
        room = player.room
        if not room: return
        chessboard = room.chessboard
        if not chessboard: return
        chessboard.killPieces(player)
        player.isAlive = False
        if room.getTurnPlayer() == player:
            room.nextTurn()
    
    '''
    Find room by its ID
    '''
    def __findRoomById(self, roomId: int):
        for r in self.rooms:
            if r.roomId == roomId:
                return r
        return None

    '''
    Get player socket ID and name in a room
    '''
    def __getPlayerSocketName(self, room):
        data = []
        for p in room.players:
            data.append([p.socketId, p.name])
        return data

    def makePlayer(self, socketId: int, name: string) -> bool:
        player = Player.createPlayer(socketId, name)
        self.socketPlayerMap[socketId] = player
        return player
    
    def makeRoom(self, host: Player) -> Room:
        chessboard = Chessboard(8) #8x8 board
        roomId = random.randint(100000, 999999)
        room = Room(roomId, host, chessboard)
        self.rooms.append(room)
        return room

    def joinRoom(self, player: Player, roomId: int) -> bool:
        # Find room that matches with the ID
        room = None
        for r in self.rooms:
            if r.roomId == roomId:
                room = r
                break
        
        # If there is no room that matches with the ID
        if room == None:
            return False

        # If there is people with same name in room
        if room.getPlayerByName(player.name):
            return False

        # If the match is started already
        if room.start:
            return False
        
        # If the player joins the room successfully
        return room.joinPlayer(player)
    
    '''
    Start Game
    '''
    def startGame(self, playerSocketId: int, roomId: int):
        room = self.__findRoomById(roomId)
        player = self.getPlayerBySocketId(playerSocketId)
        
        # If room does not exist
        if not room:
            return False, [], None, None
        
        # If player is not the host
        if not room.isHost(player):
            return False, [], None, None

        # If game is started
        if room.startGame():
            data = self.__getPlayerSocketName(room)
            return True, data, room.chessboard.getState(), room.chessboard.getOwnerState()

        return False, [], None, None

    '''
    Get player in room
    '''
    def getPlayerInRoom(self, roomId: int):
        room = self.__findRoomById(roomId)
        player = self.__getPlayerSocketName(room)
        return player


    def getPlayerBySocketId(self, socketId: int) -> Player:
        return self.socketPlayerMap[socketId]

    '''
    Give star to player by socket ID
    For testing
    '''
    def giveStar(self, playerSocketId: int, amount: int):
        player = self.getPlayerBySocketId(playerSocketId)
        player.star += amount
        
    '''
    Constants
    '''
    R_PLAYER_DISCONNECT_OK = 1
    R_PLAYER_DISCONNECT_NOT_OK = 2
