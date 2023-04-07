'''
Eat own pawn test
When a player tries to eat his own pawn
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6000, "Jack")
    game.enterRoom(6001, "Peter", roomId)
    game.startGame(6000, roomId)

    # Jack click his pawn on position (0, 2) and server gives available move as response
    moves = game.getPieceMove(roomId, 0, 2)

    # Jack have pawn in (1, 3)
    # Jack move his pawn to (1, 3). This is eating move.
    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6000, 0, 2, 1, 3)
    assert chessboardState == None, "Friendly fire"

def eatOwnPawnTest():
    try:
        run()
        return True
    except Exception as e:
        print("eatOwnPawnTest: " + str(e))
        return False
