'''
Promote pawn test
When a player promote his pawn
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

    # Give 3 star to jack (for testing purpose)
    game.giveStar(6000, 3)

    # Jack pay 3 star to promote his pawn on position (0, 2)
    chessboardState, nextTurn, ownerState, playerList, starData = game.promotePawn(6000, 0, 2, "h")
    
    assert chessboardState != None, "Promoting pawn failed"
    assert nextTurn == [6001, "Peter"], "Turn is not changed"

def promotePawnTest():
    try:
        run()
        return True
    except Exception as e:
        print("promotePawnTest: " + str(e))
        return False
