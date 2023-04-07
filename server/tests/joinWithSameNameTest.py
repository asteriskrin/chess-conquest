'''
Join with same name test
Checking if there are 2 people with the same name try to join to a room
'''

from Game.GameController import GameController

def run():
    # Server program is started
    game = GameController()

    # A client with socket ID 6000 creates a room
    roomId = game.createRoom(6000, "Lily34")

    # A client with socket ID 6001 joins the room
    checkRoomId, data = game.enterRoom(6001, "Lily34", roomId)

    assert checkRoomId == -1, "Player with same name can join a room."


def joinWithSameNameTest():
    try:
        run()
        return True    
    except Exception as e:
        print("joinWithSameNameTest: " + str(e))
    return False