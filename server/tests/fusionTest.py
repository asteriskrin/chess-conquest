'''
Fusion test
When a player fusion his pieces
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6000, "Jack")
    game.enterRoom(6001, "Peter", roomId)
    game.startGame(6000, roomId)

    # Jack fusion 3 pawns for a horse and place the horse to (5, 5)
    chessboardState, nextTurn, ownerState, playerList = game.fusionPiece(6000, "h", 5, 5)
    
    assert chessboardState != None, "Fusion pawn failed"
    assert nextTurn == [6001, "Peter"], "Turn is not changed"

def fusionTest():
    try:
        run()
        return True
    except Exception as e:
        print("fusionTest: " + str(e))
        return False
