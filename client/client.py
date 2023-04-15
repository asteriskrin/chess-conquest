import socket
import json
from threading import Thread
from frontend.GameFrontend import GameFrontend
import time
from dotenv import dotenv_values

# Load setting
setting = dotenv_values('.setting')

# Macro State
# Defining current action state
STATE_DOING_NOTHING = 0
STATE_PICKING_UP_PIECE = 1
STATE_BUYING_PAWN = 2
STATE_FUSE = 3
STATE_PROMOTE = 4

# Global variable to store chess window instance
# Default is None because it is not opened yet
gameFrontend = None
chessWindow = None
mainMenuWindow = None
serverSocket = None
roomPlayers = []
myRoomId = 0
turnPlayerName = None
currentState = STATE_DOING_NOTHING
selectedPiece = None
playerName = ""
isGameStarted = False
pieceChange = ""
# Callback when chess box is clicked


def onClickChessBox(x, y):
    global chessWindow
    global turnPlayerName
    global serverSocket
    global selectedPiece, isGameStarted, currentState, pieceChange

    # Prevent player from clicking chessboard if the game is not started yet
    if not isGameStarted:
        return

    # If it is not the player turn, prevent from doing anything on chessboard
    if playerName != turnPlayerName:
        chessWindow.setPopUpMessage("It is not your turn right now.")
        return

    if currentState == STATE_BUYING_PAWN:
        if chessWindow.ownerState[x][y] == None:
            buyPawn(serverSocket, x, y)
        else:
            chessWindow.setPopUpMessage("That box is not empty.")
        currentState = STATE_DOING_NOTHING
        chessWindow.hideMovementHighlight()
    elif currentState == STATE_FUSE:
        if pieceChange:
            if chessWindow.ownerState[x][y] == None:
                # Ganti ke fungsi fusion
                fusePiece(serverSocket, x, y, pieceChange)
                currentState = STATE_DOING_NOTHING
                pieceChange = ""
    elif currentState == STATE_PROMOTE:
        if not selectedPiece:
            chessWindow.setPopUpMessage(
                "Please Choose The Promoted Piece Option Below")
            if chessWindow.ownerState[x][y] == playerName:
                selectedPiece = [x, y]
            else:
                chessWindow.chatBox.addChat(
                    "System", "You don't own this piece.")
    else:
        if selectedPiece:
            if [x, y] in chessWindow.chessboardSection.highlight:
                movePiece(serverSocket,
                          selectedPiece[0], selectedPiece[1], x, y)
            selectedPiece = None
            chessWindow.hideMovementHighlight()
        else:
            if chessWindow.ownerState:
                if chessWindow.ownerState[x][y]:
                    if chessWindow.ownerState[x][y] == playerName:
                        if turnPlayerName == playerName:
                            checkMove(serverSocket, x, y)
                            selectedPiece = [x, y]
                        else:
                            print("This is your piece, but it is not your turn right now, please wait for {} to make move.".format(
                                turnPlayerName))
                    else:
                        print("This is {}'s piece, this is not yours.".format(
                            chessWindow.ownerState[x][y]))
                else:
                    print("No one owns this piece.")

# Callback when piece button is clicked
def onPieceButtonSelected(pieceType):
    global serverSocket, currentState, pieceChange, selectedPiece, turnPlayerName
    # Prevent from doing anything if it is not the turn
    if playerName != turnPlayerName and pieceType != "START_BUTTON":
        chessWindow.setPopUpMessage("It is not your turn right now.")
        return
    print(pieceType)
    if pieceType == "START_BUTTON":
        hostStartGame(serverSocket)
    elif pieceType == "BUY_PAWN_BUTT":
        if currentState != STATE_BUYING_PAWN:
            currentState = STATE_BUYING_PAWN
            chessWindow.setPopUpMessage(
                "Please Choose Where To Put Your New Pawn")
            chessWindow.emptyHighlight()
        else:
            currentState = STATE_DOING_NOTHING
            chessWindow.setPopUpMessage(
                "{}, You can move your piece now".format(turnPlayerName))
            chessWindow.hideMovementHighlight()
    elif pieceType == "FUSE_BUTTON":
        if currentState != STATE_FUSE:
            currentState = STATE_FUSE
            chessWindow.setPopUpMessage(
                "Please Choose The Fused Piece Option Below")
        else:
            currentState = STATE_DOING_NOTHING
            chessWindow.setPopUpMessage(
                "{}, You can move your piece now".format(turnPlayerName))
    elif pieceType == "PROMOTE_BUTTON":
        if currentState != STATE_PROMOTE:
            currentState = STATE_PROMOTE
            chessWindow.setPopUpMessage(
                "Please Select The Pawn You Want To Promote")
        else:
            currentState = STATE_DOING_NOTHING
            chessWindow.setPopUpMessage(
                "{}, You can move your piece now".format(turnPlayerName))
    elif pieceType == "Castle":
        if currentState != STATE_DOING_NOTHING:
            pieceChange = "c"
        if currentState == STATE_FUSE:
            chessWindow.setPopUpMessage(
                "Please Select Where To Put The {}".format(pieceType))
        elif currentState == STATE_PROMOTE:
            clientPromotePawn("c")
    elif pieceType == "Horse":
        if currentState != STATE_DOING_NOTHING:
            pieceChange = "h"
        if currentState == STATE_FUSE:
            chessWindow.setPopUpMessage(
                "Please Select Where To Put The {}".format(pieceType))
        elif currentState == STATE_PROMOTE:
            clientPromotePawn("h")
    elif pieceType == "Bishop":
        if currentState != STATE_DOING_NOTHING:
            pieceChange = "m"
        if currentState == STATE_FUSE:
            chessWindow.setPopUpMessage(
                "Please Select Where To Put The {}".format(pieceType))
        elif currentState == STATE_PROMOTE:
            clientPromotePawn("m")
    elif pieceType == "Queen":
        if currentState != STATE_DOING_NOTHING:
            pieceChange = "q"
        if currentState == STATE_FUSE:
            chessWindow.setPopUpMessage(
                "Please Select Where To Put The {}".format(pieceType))
        elif currentState == STATE_PROMOTE:
            clientPromotePawn("q")

def clientPromotePawn(pieceType):
    global serverSocket, currentState, selectedPiece
    if selectedPiece:
        promotePiece(
            serverSocket, selectedPiece[0], selectedPiece[1], pieceType)
        selectedPiece = None
    currentState = STATE_DOING_NOTHING


def onChat(message):
    global serverSocket
    sendChat(serverSocket, message)

# Threaded function to receive message from server
def recvMsg(sock):
    # Use chessWindow global variable
    global chessWindow
    global myRoomId
    global turnPlayerName, mainMenuWindow, isGameStarted
    global gameFrontend

    while True:
        data = sock.recv(2048)
        data = json.loads(data.decode())
        response = data["RESPONSE"]
        body = data["DATA"]

        if(response == "ROOM_CREATED"):
            print("Room Created")
            print("Room ID: " + str(body["ROOM_ID"]))
            myRoomId = int(body["ROOM_ID"])
            chessWindow = gameFrontend.openChessGameWindow(
                onPieceButtonSelected, onClickChessBox, onChat)
            time.sleep(3)
            chessWindow.setRoomId(str(myRoomId))
            chessWindow.setPopUpMessage(
                "Waiting for players... (1/4) ")
            roomPlayers.append(playerName)

            # Player Star Info
            playerStarData = []
            for p in roomPlayers:
                playerStarData.append([p, 0])
            chessWindow.playerInfoBox.setPlayerData(playerStarData)

        elif(response == "ROOM_NOT_CREATED"):
            gameFrontend.getWin().setRoomErrorText(body["REASON"])

        elif(response == "JOIN_ROOM_SUCCESS"):
            print("Joined Room")
            print(body)
            chessWindow = gameFrontend.openChessGameWindow(
                onPieceButtonSelected, onClickChessBox, onChat)
            chessWindow.setRoomId(str(myRoomId))
            playerListStr = ""
            for p in body:
                playerListStr += p[1] + " "
                roomPlayers.append(p[1])
            if len(roomPlayers) == 4:
                chessWindow.setPopUpMessage(
                    "Room full ({}/4) {}".format(len(body), playerListStr))
            else:
                chessWindow.setPopUpMessage(
                    "Waiting for players... ({}/4) {}".format(len(body), ""))
            chessWindow.destroyStartButton()

            # Player Star Info
            playerStarData = []
            for p in roomPlayers:
                playerStarData.append([p, 0])
            chessWindow.playerInfoBox.setPlayerData(playerStarData)

        elif(response == "OTHER_PLAYER_JOIN"):
            print(body["NAME"] + " Joined")
            print("Player {} has joined the room.".format(body["NAME"]))
            roomPlayers.append(body["NAME"])

            playerListStr = ""
            for name in roomPlayers:
                playerListStr += name + " "
            if len(roomPlayers) == 4:
                chessWindow.setPopUpMessage(
                    "Room full ({}/4) {}".format(len(roomPlayers), playerListStr))
            else:
                chessWindow.setPopUpMessage(
                    "Waiting for players... ({}/4) {}".format(len(roomPlayers), playerListStr))

            # Player Star Info
            playerStarData = []
            for p in roomPlayers:
                playerStarData.append([p, 0])
            chessWindow.playerInfoBox.setPlayerData(playerStarData)

        elif(response == "GAME_STARTED"):
            isGameStarted = True

            turnPlayerName = body["TURN"]
            chessboardState = body["CHESSBOARD_STATE"]
            ownerState = body["OWNER_STATE"]
            if turnPlayerName == playerName:
                chessWindow.setPopUpMessage(
                    "{}, it is your turn now!".format(playerName))
            else:
                chessWindow.setPopUpMessage(
                    "It is {}'s turn now.".format(turnPlayerName))
            print("Game has been started. It is {}'s turn now.".format(turnPlayerName))
            chessWindow.setBoardState(chessboardState, ownerState)
            chessWindow.destroyStartButton()

        elif(response == "GAME_NOT_STARTED"):
            print("You can not start game: {}".format(body["REASON"]))

        elif(response == "MOVE_SUCCESS"):
            winner = body["WINNER"]
            chessWindow.setBoardState(
                body["CHESSBOARD_STATE"], body["CHESSBOARD_OWNER_STATE"])
            # Player Star Info
            chessWindow.playerInfoBox.setPlayerData(body["STAR_DATA"])
            if winner:
                # Prevent user click
                isGameStarted = False
                chessWindow.chatBox.addChat("System", "Game over.")
                chessWindow.chatBox.addChat("System", "{} wins.".format(winner))
            else:
                chessWindow.setPopUpMessage(
                    "It is {}'s turn now".format(body["NEXT_PLAYER"][1]))
                turnPlayerName = body["NEXT_PLAYER"][1]

        elif(response == "MOVE_FAILED"):
            print(body["REASON"])
            chessWindow.setPopUpMessage(body["REASON"])

        elif(response == "AVAILABLE_MOVE"):
            chessWindow.hideMovementHighlight()
            chessWindow.showMovementHighlight(body)

        elif(response == "NO_AVAILABLE_MOVE"):
            print(body["REASON"])

        # Receiving chat
        elif response == "RECEIVE_CHAT":
            personName = body["NAME"]
            message = body["MESSAGE"]

            chessWindow.chatBox.addChat(personName, message)

        # Join Room Failed
        elif response == "JOIN_ROOM_FAILED":
            gameFrontend.getWin().setRoomErrorText("Room Code not found")

        # Buy Pawn Failed
        elif response == "BUY_FAILED":
            chessWindow.setPopUpMessage(body["REASON"])

        # Buy Pawn Success
        elif response == "BUY_SUCCESS":
            chessWindow.setBoardState(
                body["CHESSBOARD_STATE"], body["CHESSBOARD_OWNER_STATE"])
            chessWindow.setPopUpMessage(
                "It is {}'s turn now".format(body["NEXT_PLAYER_DATA"][1]))
            turnPlayerName = body["NEXT_PLAYER_DATA"][1]

            # Player Star Info
            chessWindow.playerInfoBox.setPlayerData(body["STAR_DATA"])

        elif response == "FUSION_SUCCESS":
            chessWindow.setBoardState(
                body["CHESSBOARD_STATE"], body["CHESSBOARD_OWNER_STATE"])
            chessWindow.setPopUpMessage(
                "It is {}'s turn now".format(body["NEXT_PLAYER_DATA"][1]))
            turnPlayerName = body["NEXT_PLAYER_DATA"][1]

        elif response == "FUSION_FAILED":
            chessWindow.setPopUpMessage(body["REASON"])

        elif response == "PROMOTE_SUCCESS":
            chessWindow.setBoardState(
                body["CHESSBOARD_STATE"], body["CHESSBOARD_OWNER_STATE"])
            chessWindow.setPopUpMessage(
                "It is {}'s turn now".format(body["NEXT_PLAYER_DATA"][1]))
            turnPlayerName = body["NEXT_PLAYER_DATA"][1]

            # Player Star Info
            chessWindow.playerInfoBox.setPlayerData(body["STAR_DATA"])

        elif response == "PROMOTE_FAILED":
            chessWindow.setPopUpMessage(body["REASON"])

        elif response == "GAME_OVER_DISCONNECTED":
            chessWindow.setPopUpMessage(
                "Game over Because Disconnected: The Winner is {}".format(body["WINNER"][1]))
            # To prevent user click after game over
            isGameStarted = False

        elif response == "PLAYER_DISCONNECTED":
            if body["NEW_HOST"]:
                if playerName == body["NEW_HOST"]:
                    chessWindow.showStartButton()
            if body["CHESSBOARD_STATE"] != None and body["CHESSBOARD_OWNER_STATE"] != None:
                turnPlayerName = body["NEXT_TURN"][1]
                chessWindow.setPopUpMessage(
                    "Player disconnected: {}".format(body["WHO_DISCONNECT"]))
                chessWindow.setBoardState(
                    body["CHESSBOARD_STATE"], body["CHESSBOARD_OWNER_STATE"])
            chessWindow.playerInfoBox.setPlayerData(body["STAR_DATA"])
            for i, p in enumerate(roomPlayers):
                if p == body["WHO_DISCONNECT"]:
                    del roomPlayers[i]
                    break

# Function to create room
def createRoom(serverSocket, playerName):
    data = {
        "COMMAND": "CREATE_ROOM",
        "DATA": {
            "NAME": playerName
        }
    }
    serverSocket.send(json.dumps(data).encode())

# Function to join room
def joinRoom(serverSocket, playerName):
    data = {
        "COMMAND": "JOIN_ROOM",
        "DATA": {
            "ROOM_ID": myRoomId,
            "NAME": playerName
        }
    }
    serverSocket.send(json.dumps(data).encode())


def hostStartGame(sock):
    data = {
        "COMMAND": "START_GAME",
        "DATA": {
            "ROOM_ID": myRoomId
        }
    }
    sock.send(json.dumps(data).encode())


def movePiece(sock, sx, sy, fx, fy):
    global myRoomId
    data = {
        "COMMAND": "MOVE",
        "DATA": {
            "ROOM_ID": myRoomId,
            "NAME": playerName,
            "MOVE": {
                "sx": sx,
                "sy": sy,
                "fx": fx,
                "fy": fy
            }
        }
    }
    sock.send(json.dumps(data).encode())


def checkMove(sock, x, y):
    global myRoomId
    data = {
        "COMMAND": "CHECK_MOVE",
        "DATA": {
            "ROOM_ID": myRoomId,
            "X": x,
            "Y": y
        }
    }
    sock.send(json.dumps(data).encode())

# function to fusion piece
def fusePiece(sock, x, y, pieceType):
    global myRoomId
    data = {
        "COMMAND": "FUSION",
        "DATA": {
            "ROOM_ID": myRoomId,
            "X": x,
            "Y": y,
            "PIECE_TYPE": pieceType
        }
    }
    sock.send(json.dumps(data).encode())

# function to promote piece
def promotePiece(sock, x, y, pieceType):
    global myRoomId
    data = {
        "COMMAND": "PROMOTE",
        "DATA": {
            "ROOM_ID": myRoomId,
            "X": x,
            "Y": y,
            "PIECE_TYPE": pieceType
        }
    }
    sock.send(json.dumps(data).encode())


'''
Function to send a chat
'''
def sendChat(sock, message):
    global myRoomId
    data = {
        "COMMAND": "SEND_CHAT",
        "DATA": {
            "ROOM_ID": myRoomId,
            "NAME": playerName,
            "MESSAGE": message
        }
    }
    sock.send(json.dumps(data).encode())

def buyPawn(sock, x, y):
    global myRoomId
    data = {
        "COMMAND": "BUY",
        "DATA": {
            "X": x,
            "Y": y
        }
    }
    sock.send(json.dumps(data).encode())

def connectToServer(playerName):
    # Instantiate socket for connection to server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Server configuration
    SERVER_IP_ADDRESS = setting['SERVER_IP']
    SERVER_PORT = int(setting['SERVER_PORT'])

    # Connect to the server
    status = server.connect((SERVER_IP_ADDRESS, SERVER_PORT))

    return server


'''
Establish connection
'''
def establishConnection():
    global serverSocket, playerName
    serverSocket = connectToServer(playerName)

    # Run a thread to standby receiving message from server
    recvThread = Thread(target=recvMsg, args=(serverSocket,))
    recvThread.start()

def onMainMenuButtonClick(buttonName):
    global mainMenuWindow, serverSocket, playerName, myRoomId
    mainMenuWindow = gameFrontend.getWin()
    if buttonName == "NAME_SUBMIT":
        playerName = mainMenuWindow.getNameInput()
        if len(playerName) < 3:
            mainMenuWindow.setNameInputErrorText("Name minimal 3 characters")
        elif not playerName.isalnum():
            mainMenuWindow.setNameInputErrorText("Name must be alphanumeric")
        else:
            mainMenuWindow.showRoomMenu()
            mainMenuWindow.setPlayerNameInWelcome(playerName)
    elif buttonName == "CREATE_ROOM":
        createRoom(serverSocket, playerName)
    elif buttonName == "JOIN_ROOM":
        myRoomId = mainMenuWindow.getRoomCodeInput()
        if not myRoomId or len(str(myRoomId)) < 6:
            mainMenuWindow.setRoomErrorText("Room Code invalid")
        else:
            joinRoom(serverSocket, playerName)

def guiThread():
    global gameFrontend
    gameFrontend = GameFrontend()
    gameFrontend.openMainMenuWindow(onMainMenuButtonClick)
    establishConnection()
    gameFrontend.runLoop()


'''
Python main program section
'''
if __name__ == "__main__":
    guiThread = Thread(target=guiThread)
    guiThread.start()
