'''
Buy pawn test
When a player buy a pawn
'''

from Game.GameController import GameController

def run():
    game = GameController()

    # Jack creates room
    roomId = game.createRoom(6000, "Jack")
    
    # Peter enters room
    game.enterRoom(6001, "Peter", roomId)

    # Jack press start game
    game.startGame(6000, roomId)

    # Give 1 star to jack (for testing purpose)
    game.giveStar(6000, 1)

    # Jack pay 1 star to buy a pawn on position (5, 2)
    chessboardState, nextTurn, ownerState, playerList, starData = game.buyPawn(6000, 5, 2)
    
    assert chessboardState != None, "Buying pawn failed"
    assert nextTurn == [6001, "Peter"], "Turn is not changed"

def buyPawnTest():
    try:
        run()
        return True
    except Exception as e:
        print("buyPawnTest: " + str(e))
        return False
