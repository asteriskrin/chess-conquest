'''
Room test
Checking room operability
'''

from Game.GameController import GameController

def run():
    # Server program is started
    game = GameController()

    # A client with socket ID 6000 creates a room
    roomId = game.createRoom(6000, "Lily")

    # A client with socket ID 6001 joins the room
    checkRoomId, data = game.enterRoom(6001, "Mila", roomId)
    assert checkRoomId == roomId, "Mila can not enter correct room ID"
    assert [6000, "Lily"] in data, "Lily is not in response data" 

    # A client with socket ID 6003 joins the room
    checkRoomId, data = game.enterRoom(6003, "Tama", roomId)
    assert checkRoomId == roomId, "Tama can not enter correct room ID"
    assert [6000, "Lily"] in data, "Lily is not in response data"
    assert [6001, "Mila"] in data, "Mila is not in response data"


    # A client with socket ID 6004 joins the room
    checkRoomId, data = game.enterRoom(6004, "Rin", roomId)
    assert checkRoomId == roomId, "Rin can not enter correct room ID"
    assert [6000, "Lily"] in data, "Lily is not in response data"
    assert [6001, "Mila"] in data, "Mila is not in response data"
    assert [6003, "Tama"] in data, "Tama is not in response data"

    # A client with socket ID 6005 tries to join the room, 
    # but it is failed because the room is full
    checkRoomId, data = game.enterRoom(6005, "Shino", roomId)
    assert checkRoomId == -1, "Shino can enter room"

    # Lily presses start button and the game is started
    response, data, chessboardState, ownerState = game.startGame(6000, roomId)
    assert response, "Lily presses start button but the game is not started."
    assert [6000, "Lily"] in data, "Lily is not in response data"
    assert [6001, "Mila"] in data, "Mila is not in response data"
    assert [6003, "Tama"] in data, "Tama is not in response data"
    assert [6004, "Rin"] in data, "Tama is not in response data"

    # Lily gets disconnected / exits the game during gameplay
    response, data = game.playerDisconnect(6000)

    # Lily tries to join the room again. But the match is already started so that she can not join
    # Lily socket ID (6008) is different because Lily reconnect
    checkRoomId, data = game.enterRoom(6008, "Rin", roomId)
    assert checkRoomId == -1, "Lily can join room while the match is started already"

def roomTest():
    try:
        run()
        return True    
    except Exception as e:
        print("roomTest: " + str(e))
    return False