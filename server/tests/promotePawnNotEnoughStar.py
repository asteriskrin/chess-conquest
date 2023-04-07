'''
Promote pawn test
When a player promote his pawn but he does not have enough star points
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

    # Give 2 star to jack (for testing purpose)
    game.giveStar(6000, 2)

    # Jack pay 3 star to promote his pawn on position (0, 2)
    chessboardState, nextTurn, ownerState, playerList, starData = game.promotePawn(6000, 0, 2, "h")
    
    assert not chessboardState, "Promoting pawn successful"
    assert nextTurn == [None, None], "Turn is changed"

def promotePawnNotEnoughStar():
    try:
        run()
        return True
    except Exception as e:
        print("promotePawnNotEnoughStar: " + str(e))
        return False
