'''
Disconnect test
Check disconnect functionality when the turn player is disconnected
'''

from Game.GameController import GameController

def run():
    # Server program is started
    game = GameController()

    # A client with socket ID 6000 creates a room
    roomId = game.createRoom(6000, "Lily")

    # A client with socket ID 6001 joins the room
    checkRoomId, data = game.enterRoom(6001, "Mila", roomId)

    # Start game
    game.startGame(6000, roomId)

    # Lily gets disconnected / exits the game during gameplay
    response, data = game.playerDisconnect(6000)

    assert data["WINNER"] != None, "Winner is not assigned"


def disconnectAtTurnTest():
    try:
        run()
        return True    
    except Exception as e:
        print("disconnectAtTurnTest: " + str(e))
    return False