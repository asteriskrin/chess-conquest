'''
Disconnect test
Check disconnect functionality
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

    # Lily gets disconnected / exits the game during gameplay
    response, data = game.playerDisconnect(6000)

    assert data["WINNER"] == None, "Winner is assigned while there is still another player in the room"

    # Mila gets disconnected / exits the game during gameplay
    response, data = game.playerDisconnect(6001)

    assert data["WINNER"] == None, "Winner is assigned while there is still another player in the room"

    # Rin gets disconnected / exits the game during gameplay
    response, data = game.playerDisconnect(6004)

    # Tama should be the winner
    assert data["WINNER"] == [6003, "Tama"], "Tama is not the winner"


def disconnectWinnerTest():
    try:
        run()
        return True    
    except Exception as e:
        print("disconnectWinnerTest: " + str(e))
    return False