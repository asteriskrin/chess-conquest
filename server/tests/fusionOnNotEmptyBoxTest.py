'''
Fusion on not empty box test
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6000, "Jack")
    game.enterRoom(6001, "Peter", roomId)
    game.startGame(6000, roomId)

    # Jack fusion 3 pawns for a horse and place the horse to (7, 2)
    chessboardState, nextTurn, ownerState, playerList = game.fusionPiece(6000, "h", 7, 2)
    
    assert chessboardState == None, "Fusion on not empty box successful"
    assert nextTurn == [None, None], "Turn is changed"

def fusionOnNotEmptyBoxTest():
    try:
        run()
        return True
    except Exception as e:
        print("fusionOnNotEmptyBoxTest: " + str(e))
        return False
