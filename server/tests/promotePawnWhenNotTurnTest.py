'''
Promote pawn when not turn test
When a player promote his pawn but it is not his turn
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

    # Give 3 star to Peter (for testing purpose)
    game.giveStar(6001, 3)

    # Peter pay 3 star to promote his pawn on position (7, 2)
    chessboardState, nextTurn, ownerState, playerList, starData = game.promotePawn(6001, 7, 2, "h")
    
    assert not chessboardState, "Promoting pawn successful"

def promotePawnWhenNotTurnTest():
    try:
        run()
        return True
    except Exception as e:
        print("promotePawnWhenNotTurnTest: " + str(e))
        return False
