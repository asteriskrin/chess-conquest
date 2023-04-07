'''
Start Game Test
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6071, "Jack")
    game.enterRoom(6082, "Peter", roomId)
    status, data, chessboardState, ownerState = game.startGame(6071, roomId)

    assert status == True, "Game is not started" 

def startGameTest():
    try:
        run()
        return True
    except Exception as e:
        print("startGameTest: " + str(e))
        return False
