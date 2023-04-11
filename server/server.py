import socket
import threading
import json
from dotenv import dotenv_values

from Game.GameController import GameController
from Game.Player import Player
from Game.Room import Room
from Game.Chessboard import Chessboard

# Load environment variables
config = dotenv_values(".env")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ipAddress = config['SERVER_IP']
port = int(config['SERVER_PORT'])
print(fr"Server is started on {ipAddress}:{port}")
server.bind((ipAddress, port))
server.listen(100)

listOfClients = []
players = {}
data = {}

game = GameController()
player = Player()


def clientThread(conn, addr):
    while True:
        try:
            message = json.loads(conn.recv(2048).decode())

            if message:

                # Create Room
                if (message["COMMAND"] == 'CREATE_ROOM'):
                    roomId = game.createRoom(
                        int(addr[1]), message["DATA"]["NAME"])

                    if (roomId != -1):
                        data = {
                            "RESPONSE": "ROOM_CREATED",
                            "DATA": {
                                "ROOM_ID": roomId
                            }
                        }
                        print("Player {}:{} has created a room ID {}".format(
                            addr[0], addr[1], roomId))
                    else:
                        data = {
                            "RESPONSE": "ROOM_NOT_CREATED",
                            "DATA": {
                                "REASON": "Fail to create room"
                            }
                        }
                        print("Player {}:{} has failed to create a room".format(
                            addr[0], addr[1]))

                    data = json.dumps(data)
                    broadcastSender(data, conn)

                # Join Room
                elif (message["COMMAND"] == "JOIN_ROOM"):

                    roomId, roomData = game.enterRoom(
                        int(addr[1]), message["DATA"]["NAME"], message["DATA"]["ROOM_ID"])

                    if (roomId != -1):
                        data = {
                            "RESPONSE": "JOIN_ROOM_SUCCESS",
                            "DATA": roomData
                        }

                        dataToOther = {
                            "RESPONSE": "OTHER_PLAYER_JOIN",
                            "DATA": {
                                "NAME": message["DATA"]["NAME"],
                            }
                        }

                        otherPlayerSocketIds = []
                        for p in roomData:
                            if p[1] != message["DATA"]["NAME"]:
                                otherPlayerSocketIds.append(p[0])

                        dataToOther = json.dumps(dataToOther)
                        broadcastToSocketIds(dataToOther, otherPlayerSocketIds)

                    else:
                        data = {
                            "RESPONSE": "JOIN_ROOM_FAILED",
                            "DATA": {
                                "REASON": "Fail to join room"
                            }
                        }
                    data = json.dumps(data)
                    broadcastSender(data, conn)

                # Start Game
                elif(message["COMMAND"] == "START_GAME"):
                    gameStart, roomData, chessboardState, ownerState = game.startGame(
                        int(addr[1]), message["DATA"]["ROOM_ID"])

                    if(gameStart):
                        # Construct response data
                        data = {
                            "RESPONSE": "GAME_STARTED",
                            "DATA": {
                                "TURN": roomData[0][1],
                                "CHESSBOARD_STATE": chessboardState,
                                "OWNER_STATE": ownerState
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Collect socket IDs
                        socketIds = []
                        for player in roomData:
                            socketIds.append(player[0])
                        # Broadcast to room
                        broadcastToSocketIds(data, socketIds)
                    else:
                        # Construct response data
                        data = {
                            "RESPONSE": "GAME_NOT_STARTED",
                            "DATA": {
                                "REASON": "Fail to start game"
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to sender
                        broadcastSender(data, conn)

                # Check Available Move
                elif (message["COMMAND"] == "CHECK_MOVE"):
                    listAvailableMove = game.getPieceMove(
                        message["DATA"]["ROOM_ID"], message["DATA"]["X"], message["DATA"]["Y"])

                    if(len(listAvailableMove) > 0):
                        data = {
                            "RESPONSE": "AVAILABLE_MOVE",
                            "DATA": listAvailableMove
                        }
                    else:
                        data = {
                            "RESPONSE": "NO_AVAILABLE_MOVE",
                            "DATA": {
                                "REASON": "No available move"
                            }
                        }

                    data = json.dumps(data)
                    broadcastSender(data, conn)

                # Move
                elif (message["COMMAND"] == "MOVE"):
                    position = message["DATA"]["MOVE"]
                    sx = position["sx"]
                    sy = position["sy"]
                    fx = position["fx"]
                    fy = position["fy"]

                    chessboardState, nextPlayerData, chessboardOwnerState, playerInRoom, playerStarData, winner = game.playerMovePiece(
                        int(addr[1]), sx, sy, fx, fy)

                    if chessboardState == None:
                        # Construct response data
                        data = {
                            "RESPONSE": "MOVE_FAILED",
                            "DATA": {
                                "REASON": "Fail to move"
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to sender
                        broadcastSender(data, conn)
                    else:
                        # Construct response data
                        data = {
                            "RESPONSE": "MOVE_SUCCESS",
                            "DATA": {
                                "NEXT_PLAYER": nextPlayerData,
                                "CHESSBOARD_STATE": chessboardState,
                                "CHESSBOARD_OWNER_STATE": chessboardOwnerState,
                                "STAR_DATA": playerStarData,
                                "WINNER": winner
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Collect socket Ids in room
                        socketIds = []
                        for player in playerInRoom:
                            socketIds.append(player[0])
                        # Broadcast to room
                        broadcastToSocketIds(data, socketIds)

                # Buy Pawn
                elif (message["COMMAND"] == "BUY"):
                    chessboardState, nextPlayerData, chessboardOwnerState, playerInRoom, playerStarData = game.buyPawn(
                        int(addr[1]), message["DATA"]["X"], message["DATA"]["Y"])

                    if chessboardState == None:
                        # Construct response data
                        data = {
                            "RESPONSE": "BUY_FAILED",
                            "DATA": {
                                "REASON": "Fail to buy"
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to sender
                        broadcastSender(data, conn)
                    else:
                        # Construct response data
                        data = {
                            "RESPONSE": "BUY_SUCCESS",
                            "DATA": {
                                "CHESSBOARD_STATE": chessboardState,
                                "NEXT_PLAYER_DATA": nextPlayerData,
                                "CHESSBOARD_OWNER_STATE": chessboardOwnerState,
                                "STAR_DATA": playerStarData
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to player in room
                        socketIds = []
                        for p in playerInRoom:
                            socketIds.append(p[0])
                        broadcastToSocketIds(data, socketIds)

                # Promote Pawn
                elif message["COMMAND"] == "PROMOTE":
                    chessboardState, nextPlayerData, chessboardOwnerState, playerInRoom, playerStarData = game.promotePawn(
                        addr[1], message["DATA"]["X"], message["DATA"]["Y"], message["DATA"]["PIECE_TYPE"])

                    if chessboardState == None:
                        # Construct response data
                        data = {
                            "RESPONSE": "PROMOTE_FAILED",
                            "DATA": {
                                "REASON": "Fail to promote"
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to sender
                        broadcastSender(data, conn)
                    else:
                        # Construct response data
                        data = {
                            "RESPONSE": "PROMOTE_SUCCESS",
                            "DATA": {
                                "CHESSBOARD_STATE": chessboardState,
                                "NEXT_PLAYER_DATA": nextPlayerData,
                                "CHESSBOARD_OWNER_STATE": chessboardOwnerState,
                                "STAR_DATA": playerStarData
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to player in room
                        socketIds = []
                        for p in playerInRoom:
                            socketIds.append(p[0])
                        broadcastToSocketIds(data, socketIds)

                # Fusion
                elif message["COMMAND"] == "FUSION":
                    chessboardState, nextPlayerData, chessboardOwnerState, playerInRoom = game.fusionPiece(
                        addr[1], message["DATA"]["PIECE_TYPE"], message["DATA"]["X"], message["DATA"]["Y"])

                    if chessboardState == None:
                        # Construct response data
                        data = {
                            "RESPONSE": "FUSION_FAILED",
                            "DATA": {
                                "REASON": "Fail to fusion"
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to sender
                        broadcastSender(data, conn)
                    else:
                        # Construct response data
                        data = {
                            "RESPONSE": "FUSION_SUCCESS",
                            "DATA": {
                                "CHESSBOARD_STATE": chessboardState,
                                "NEXT_PLAYER_DATA": nextPlayerData,
                                "CHESSBOARD_OWNER_STATE": chessboardOwnerState,
                            }
                        }
                        # Convert to JSON
                        data = json.dumps(data)
                        # Broadcast to player in room
                        socketIds = []
                        for p in playerInRoom:
                            socketIds.append(p[0])
                        broadcastToSocketIds(data, socketIds)

                # Sending chat
                elif message["COMMAND"] == "SEND_CHAT":
                    roomId = message["DATA"]["ROOM_ID"]
                    playerList = game.getPlayerInRoom(roomId)
                    socketIds = []
                    for player in playerList:
                        socketIds.append(player[0])
                    sendChatToSocketIds(
                        socketIds, message["DATA"]["NAME"], message["DATA"]["MESSAGE"])

        except Exception as e:
            print("Client {}:{} is disconnected from server.".format(
                addr[0], addr[1]))
            response, data = game.playerDisconnect(addr[1])
            if response:
                # Winner
                if data["WINNER"] != None:
                    # TODO: Send request to the winner telling that he is the winner
                    # data["WINNER"] is a list containing winner socket ID and winner name
                    # For example: data["WINNER"] = [6000, "Husein"]

                    # construct response data
                    response_data = {
                        "RESPONSE": "GAME_OVER_DISCONNECTED",
                        "DATA": {
                            "WINNER": data["WINNER"],
                        }
                    }

                    # convert to JSON
                    response_data = json.dumps(response_data)

                    socketIds = [data["WINNER"][0]]

                    broadcastToSocketIds(response_data, socketIds)
                else:
                    # TODO: Send request to all people in the room that:
                    # 1. Star data is updated
                    # 2. Chessboard state and chessboard owner state is updated
                    # 3. Whose turn is now
                    # Use these following variable:
                    # 1) data["NEXT_TURN"] is a list containing turn player socket ID and turn player name
                    #    For example: data["NEXT_TURN"] = [6000, "Husein"]
                    # 2) data["PLAYER_LIST"] is a list of list containing player socket ID and player name who are in the room.
                    #    For example: data["PLAYER_LIST"] = [[6000, "Husein"], [6001, "Ahdan"]]
                    # 3) data["STAR_DATA"] is a list containing player name and his star.
                    #    For example: data["STAR_DATA"] = [["Husein", 6], ["Ahdan", 3]]
                    # 4) data["CHESSBOARD_STATE"] is chessboard state
                    # 5) data["OWNER_STATE"] is chessboard owner state

                    # construct response data
                    response_data = {
                        "RESPONSE": "PLAYER_DISCONNECTED",
                        "DATA": {
                            "NEXT_TURN": data.get("NEXT_TURN"),
                            "STAR_DATA": data.get("STAR_DATA"),
                            "CHESSBOARD_STATE": data.get("CHESSBOARD_STATE"),
                            "CHESSBOARD_OWNER_STATE": data.get("OWNER_STATE"),
                            "WHO_DISCONNECT": data.get("WHO_DISCONNECT"),
                            "NEW_HOST": data.get("NEW_HOST")
                        }
                    }
                    socket_list = []
                    for player in data.get("PLAYER_LIST"):
                        socket_list.append(player[0])

                    # Convert to JSON
                    response_data = json.dumps(response_data)

                    broadcastToSocketIds(response_data, socket_list)
            break


def broadcastSender(message, connection):

    for clients in listOfClients:
        if clients == connection:
            clients.send(message.encode())
            break


def broadcast(message, connection):
    for clients in listOfClients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def broadcastToSocketIds(message, socketIds):
    for socketId in socketIds:
        try:
            players[socketId].send(message.encode())
        except:
            print("Player with socket port {} seems disconnect, he has been removed from player table.".format(
                socketId))
            del players[socketId]


def sendChatToSocketIds(socketIds, name, message):
    data = {
        "RESPONSE": "RECEIVE_CHAT",
        "DATA": {
            "NAME": name,
            "MESSAGE": message
        }
    }
    data = json.dumps(data)
    broadcastToSocketIds(data, socketIds)


def remove(connection):
    if connection in listOfClients:
        listOfClients.remove(connection)


while True:
    conn, addr = server.accept()
    print("Client {}:{} is connected to server.".format(
        addr[0], addr[1]))
    listOfClients.append(conn)

    # Dictionary works as map to map socket port to instance of socket which is O(1) implementation
    players[addr[1]] = conn

    threading.Thread(target=clientThread, args=(conn, addr)).start()
