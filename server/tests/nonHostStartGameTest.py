'''
Start Game Test
Check if player, who is not room host, tries to start the game
'''

from Game.GameController import GameController

def run():
    game = GameController()

    roomId = game.createRoom(6071, "Jack")
    game.enterRoom(6082, "Peter", roomId)
    status, data, chessboardState, ownerState = game.startGame(6082, roomId)

    assert status == False, "Game is started" 

def nonHostStartGameTest():
    try:
        run()
        return True
    except Exception as e:
        print("nonHostStartGameTest: " + str(e))
        return False
