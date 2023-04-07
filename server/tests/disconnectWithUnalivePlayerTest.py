'''
Disconnect test
Check disconnect functionality when there are unalive player
'''

from Game.GameController import GameController

def run():
    # Server program is started
    game = GameController()

    # A client with socket ID 6000 creates a room
    roomId = game.createRoom(6000, "Lily")

    # A client with socket ID 6001 joins the room
    checkRoomId, data = game.enterRoom(6001, "Mila", roomId)

    # A client with socket ID 6003 joins the room
    checkRoomId, data = game.enterRoom(6003, "Tama", roomId)

    # A client with socket ID 6004 joins the room
    checkRoomId, data = game.enterRoom(6004, "Rin", roomId)

    # Start game
    game.startGame(6000, roomId)

    # Kill Lily
    game.playerKill(6000)

    # Kill Rin
    game.playerKill(6004)

    # Tama gets disconnected / exits the game during gameplay
    response, data = game.playerDisconnect(6003)

    assert data["WINNER"] == [6001, "Mila"], "Winner is not assigned"


def disconnectWithUnalivePlayerTest():
    try:
        run()
        return True    
    except Exception as e:
        print("disconnectWithUnalivePlayerTest: " + str(e))
    return False