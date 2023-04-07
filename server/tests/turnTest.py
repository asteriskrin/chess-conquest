'''
Turn test
Check if turn is changed after player move his piece
'''

import re
from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6000, "Jack")
    game.enterRoom(6001, "Peter", roomId)
    game.startGame(6000, roomId)

    # Jack click his pawn on position (0, 2) and server gives available move as response
    moves = game.getPieceMove(roomId, 0, 2)

    # Jack move his pawn
    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6000, 0, 2, 1, 2)

    assert nextTurn == [6001, "Peter"], "Turn is not changed" 

def turnTest():
    try:
        run()
        return True
    except Exception as e:
        print("turnTest: " + str(e))
        return False
