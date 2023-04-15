'''
Chess Game Window class
'''

from threading import Thread
import pygame
from frontend.ChatBox import ChatBox
from frontend import button, chess
from frontend.ChessboardSection import ChessboardSection
from frontend.GameWindow import GameWindow
from frontend.PlayerInfoBox import PlayerInfoBox
from frontend.TextButton import TextButton

class ChessGameWindow(GameWindow):
    onPieceButtonSelected = None
    onClickChessBox = None

    def __init__(self, onPieceButtonSelected, onClickChessBox, onChatFunc):
        # Sound
        self.sound = pygame.mixer.Sound("frontend/music/knob-458.wav")

        self.roomId = ""
        self.roomIdFont = pygame.font.Font(None, 40)
        self.baseFont = pygame.font.Font(None, 24)
        # Setting up callback
        self.onPieceButtonSelected = onPieceButtonSelected
        self.onClickChessBox = onClickChessBox

        # Chessboard size
        chessWidth = 560
        chessHeight = 560

        # Chessboard dimension
        self.dimension = 8
        
        self.sqSize = chessWidth // self.dimension

        self.chessboardSection = ChessboardSection(self.sqSize, self.dimension)

        # Chat Box
        self.chatBox = ChatBox(onChatFunc)

        # Player Info Box
        self.playerInfoBox = PlayerInfoBox(650, 80)

        # Start Button
        self.showStartButton()

        # Buy Pawn Button
        self.buyPawnButt = TextButton(800, 700, 130, 40, (28, 30, 60), (255, 255, 255), (255, 255, 255), "Buy Pawn")

        # Fuse Button
        self.fuseButton = TextButton(650, 700, 130, 40, (28, 30, 60), (255, 255, 255), (255, 255, 255), "Fuse Pawn")

        #Promote Pawn Button
        self.promoteButton = TextButton(650, 750, 280, 40, (28, 30, 60), (255, 255, 255), (255, 255, 255), "Promote Pawn")        

        self.popupMessage = ""

        self.background = pygame.image.load("frontend/img/chess-5747335_1280.png")

        self.disconnectImage = pygame.image.load("frontend/img/disconnect.png")
        self.disconnect = pygame.transform.scale(self.disconnectImage,(500,300))
        self.disconnectFlag = None
        #button image
        delete_img = pygame.image.load('frontend/images/delete.png').convert_alpha()
        castle_img = pygame.image.load('frontend/images/wc.png').convert_alpha()
        horse_img = pygame.image.load('frontend/images/wh.png').convert_alpha()
        bishop_img = pygame.image.load('frontend/images/wm.png').convert_alpha()
        queen_img = pygame.image.load('frontend/images/wq.png').convert_alpha()

        self.delete_button = button.Button(80, 670, delete_img, 0.2)
        self.castle_button = button.Button(235, 670, castle_img, 0.6) 
        self.horse_button = button.Button(335, 670, horse_img, 0.6)
        self.bishop_button = button.Button(435, 670, bishop_img, 0.6)
        self.queen_button = button.Button(535, 670, queen_img, 0.6)

        #button flag
        deleteFlag = False
        castleChange = False
        horseChange = False
        bishopChange = False
        queenChange = False

        self.chessboardState = [["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"]]
        self.ownerState = None

        self.ownerColor = None

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseLocation = pygame.mouse.get_pos()
            col = (mouseLocation[0] // self.sqSize) - 1
            row = (mouseLocation[1] // self.sqSize) - 1
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                self.onClickChessBox(row, col)
        self.chatBox.handleEvent(event)
        if self.startButton and self.startButton.handleEvent(event):
            self.onPieceButtonSelected("START_BUTTON")
        if self.buyPawnButt and self.buyPawnButt.handleEvent(event):
            self.onPieceButtonSelected("BUY_PAWN_BUTT")
        if self.fuseButton and self.fuseButton.handleEvent(event):
            self.onPieceButtonSelected("FUSE_BUTTON")
        if self.promoteButton and self.promoteButton.handleEvent(event):
            self.onPieceButtonSelected("PROMOTE_BUTTON")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        self.drawMessage(screen, 150, 20, self.popupMessage, self.baseFont)
        self.drawMessageBox(screen, 200, 20)
        self.drawMessage(screen, 370, 650, "Piece Change", self.baseFont)
        self.drawMessage(screen, 90, 750, "Point Needed", self.baseFont)
        self.drawMessage(screen, 270, 750, "5", self.baseFont)
        self.drawMessage(screen, 370, 750, "3", self.baseFont)
        self.drawMessage(screen, 470, 750, "3", self.baseFont)
        self.drawMessage(screen, 570, 750, "8", self.baseFont)
        self.drawMessage(screen, 680, 20, "Room ID: " + str(self.roomId), self.roomIdFont)
        if self.castle_button.draw(screen):
            self.onPieceButtonSelected("Castle")
        if self.horse_button.draw(screen):
            self.onPieceButtonSelected("Horse")
        if self.bishop_button.draw(screen):
            self.onPieceButtonSelected("Bishop")
        if self.queen_button.draw(screen):
            self.onPieceButtonSelected("Queen")
        self.drawGameState(screen)
        self.chatBox.draw(screen)
        if self.disconnectFlag != None:
            screen.blit(self.disconnect, (250, 200))
        self.playerInfoBox.draw(screen)
        if self.startButton:
            self.startButton.draw(screen)
        if self.buyPawnButt:
            self.buyPawnButt.draw(screen)
        if self.fuseButton:
            self.fuseButton.draw(screen)
        if self.promoteButton:
            self.promoteButton.draw(screen)

    def setRoomId(self, roomId):
        self.roomId = roomId

    def setPopUpMessage(self, message):
        self.popupMessage = message

    def drawMessage(self, screen, x, y, message, font):
        popup = font.render(message, True, (255, 255, 255))
        screen.blit(popup,(x, y))

    def drawMessageBox(self, screen, x, y):
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(150, 10, 400, 40), 1)
        #pygame.display.flip()
        

    def drawGameState(self, screen):
        if self.chessboardState:
            self.chessboardSection.drawGameState(screen, self.chessboardState, self.ownerState)
            self.chessboardSection.drawHighlight(screen)

    def __getMovingPiece(self, oldState, newState):
        sx = 0
        sy = 0
        fx = 0
        fy = 0

        x = 0
        y = 0
        while x < 8:
            while y < 8:
                if oldState[x][y] != newState[x][y]:
                    sx = x
                    sy = y
                    x = 8
                    y = 8
                y += 1
            x += 1
        
        x = 0
        y = 0
        while x < 8:
            while y < 8:
                if newState[x][y] != oldState[x][y] and x != sx and y != sy:
                    fx = x
                    fy = y
                    x = 8
                    y = 8
                y += 1
            x += 1
        
        return [sx, sy, fx, fy]

    def setBoardState(self, chessboardState, ownerState):
        # This code is not optimized, it needs to be optimized in future development
        
        # Get old board state and new board state to know which piece moved
        # movingPiece = [sx, sy, fx, fy]
        # If no piece moves, movingPiece = None
        if self.chessboardState:
            movingPiece = self.__getMovingPiece(self.chessboardState, chessboardState)
            self.chessboardSection.setMovingPiece(movingPiece)

        if not self.ownerColor:
            owners = []
            for row in ownerState:
                for name in row:
                    if name and name not in owners:
                        owners.append(name)

            self.ownerColor = {}
            COLOR_LIST = ["b", "g", "r", "y"]
            color_id = 0
            for name in owners:
                self.ownerColor[name] = COLOR_LIST[color_id]
                color_id += 1

        # Add color
        for row in range(self.dimension):
            for col in range(self.dimension):
                if ownerState[row][col]:
                    chessboardState[row][col] = self.ownerColor[ownerState[row][col]] + chessboardState[row][col]

        self.chessboardState = chessboardState
        self.ownerState = ownerState
        self.sound.play()

    def showMovementHighlight(self, availableMoves):
        for move in availableMoves:
            self.chessboardSection.addHighlight(move[0], move[1])

    def hideMovementHighlight(self):
        self.chessboardSection.removeHighlight()

    def showDisconnectMessage(self):
        self.disconnectFlag = 1

    def emptyHighlight(self):
        self.chessboardSection.removeHighlight()
        # Highlight empty box
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.chessboardState[row][col] == "--":
                    self.chessboardSection.addHighlight(row, col)

    '''
    Destroy start button
    '''
    def destroyStartButton(self):
        if self.startButton:
            del self.startButton
            self.startButton = None

    
    '''
    Show start button
    '''
    def showStartButton(self):
        self.startButton = TextButton(650, 650, 280, 40, (28, 30, 60), (255, 255, 255), (255, 255, 255), "              Start Game")

    '''
    Set up callback when piece button is clicked
    '''
    def setOnPieceButtonSelected(self, func):
        self.onPieceButtonSelected = func

    '''
    Set up callback when chess box is clicked
    '''
    def setOnClickChessBox(self, func):
        self.onClickChessBox = func
    