'''
Illegal move test
When a player move his piece to illegal coordinate
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6000, "Jack")
    game.enterRoom(6001, "Peter", roomId)
    game.startGame(6000, roomId)

    # Jack click his pawn on position (0, 2) and server gives available move as response
    moves = game.getPieceMove(roomId, 0, 2)

    # Jack move his pawn to (-1, 3). This is illegal move. Negative value is out of the chessboard.
    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6000, 0, 2, -1, 3)
    assert chessboardState == None, "Pawn from (0, 2) can move to (-1, 3)"

    # Jack move his pawn to (1, 0). This is illegal move. There is nothing to eat on (1, 0)
    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6000, 0, 2, 1, 0)
    assert chessboardState == None, "Pawn from (0, 2) can move to (1, 0)"

    # Jack move his pawn to (0, 4). This is illegal move.
    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6000, 0, 2, 0, 4)
    assert chessboardState == None, "Pawn from (0, 2) can move to (0, 4)"

    # Jack move his pawn to (0, 3). This is illegal move because there is King in (0, 3).
    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6000, 0, 2, 0, 3)
    assert chessboardState == None, "Pawn from (0, 2) can move to King position (0, 3)"

def illegalMoveTest():
    try:
        run()
        return True
    except Exception as e:
        print("illegalMoveTest: " + str(e))
        return False
