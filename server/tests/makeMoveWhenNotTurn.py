'''
Make move when not turn
Check if player tries to move his piece when it is not his turn
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6000, "Jack")
    game.enterRoom(6001, "Peter", roomId)
    game.startGame(6000, roomId)

    # pPeter click his pawn on position (7, 2) and server gives available move as response
    moves = game.getPieceMove(roomId, 7, 2)

    chessboardState, nextTurn, ownerState, playerList, starData, winner = game.playerMovePiece(6001, 7, 2, 6, 2)
    assert not chessboardState, "Peter can move piece when it is not his turn."

def makeMoveWhenNotTurn():
    try:
        run()
        return True
    except Exception as e:
        print("makeMoveWhenNotTurn: " + str(e))
        return False
