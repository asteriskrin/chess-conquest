'''
Main Menu Window class
'''

import threading
import pygame
from frontend.GameWindow import GameWindow
from frontend.NameInputBox import NameInputBox
from frontend.RoomCodeInputBox import RoomCodeInputBox
from frontend.TextButton import TextButton

class MainMenuWindow(GameWindow):
    FPS_LIMIT = 20
    onButtonClickFunc = None
    

    def __init__(self, onButtonClickFunc):

        self.logoAsset = pygame.image.load("frontend/img/logo.png")
        logoWidth = self.logoAsset.get_width()
        logoHeight = self.logoAsset.get_height()
        self.imageLogo = pygame.transform.scale(self.logoAsset, (int(logoWidth*0.6), int(logoHeight*0.6)))
        self.rectLogo = self.imageLogo.get_rect()
        self.rectLogo.topleft = (275, 100)

        # On Button Click Callback
        self.onButtonClickFunc = onButtonClickFunc

        # Base Font
        self.baseFont = pygame.font.Font(None, 30)

        # Welcome Text
        self.textWelcome = None

        # Create Room
        self.createRoomButton = None

        # Join Room
        self.joinRoomButton = None

        # Room Code Input
        self.roomCodeInputBox = None

        # Room Code Text
        self.textRoomCode = None

        # Room Error Text
        self.textRoomError = None

        # Name Input Text
        self.textNameInput = self.baseFont.render("Enter username", True, (255, 255, 255))

        # Name Input Error Text
        self.nameInputErrorText = None

        # Name Input
        self.namaInputBox = NameInputBox(300, 435, 400, 30)

        # Name Submit Button
        self.nameSubmitButton = TextButton(625, 480, 75, 40, (2, 30, 60), (255, 255, 255), (255, 255, 255), "Enter")

        self.background = pygame.image.load("frontend/img/gettyimages-1041114178.jpg")
    
    def __hideNameInputMenu(self):
        self.textNameInput = None
        self.namaInputBox = None
        self.nameInputErrorText = None
        self.nameSubmitButton = None

    def showRoomMenu(self):
        # Hide Name Input
        self.__hideNameInputMenu()

        # Create Room
        self.createRoomButton = TextButton(250, 510, 235, 50, (28, 30, 60), (255, 255, 255), (255, 255, 255), "Create Room", 50)

        # Join Room
        self.joinRoomButton = TextButton(440, 400, 195, 50, (28, 30, 60), (255, 255, 255), (255, 255, 255), "Join Room", 50)

        # Room Code Input
        self.roomCodeInputBox = RoomCodeInputBox(250, 400, 180, 50)

        # Room Code Text
        self.textRoomCode = self.baseFont.render("Masukkan Room Code:", True, (255, 255, 255))

    def setPlayerNameInWelcome(self, playerName):
        self.textWelcome = self.baseFont.render("Selamat datang di Chess Conquest, {}!".format(playerName), True, (255, 255, 255))

    def setRoomErrorText(self, message):
        self.textRoomError = self.baseFont.render(message, True, (255, 255, 255))

    def setNameInputErrorText(self, message):
        self.nameInputErrorText = self.baseFont.render(message, True, (255, 255, 255))

    def getRoomCodeInput(self):
        if self.roomCodeInputBox:
            return self.roomCodeInputBox.getRoomCode()
        return 0

    def getNameInput(self):
        if self.namaInputBox:
            return self.namaInputBox.getInput()
        return ""

    def handleEvent(self, event):
        if self.createRoomButton and self.createRoomButton.handleEvent(event):
            self.onButtonClickFunc("CREATE_ROOM")
            
        
        if self.joinRoomButton and self.joinRoomButton.handleEvent(event):
            self.onButtonClickFunc("JOIN_ROOM")
            
        
        if self.roomCodeInputBox:
            self.roomCodeInputBox.handleEvent(event)
            
        
        if self.namaInputBox:
            self.namaInputBox.handleEvent(event)
            
        
        if self.nameSubmitButton and self.nameSubmitButton.handleEvent(event):
            self.onButtonClickFunc("NAME_SUBMIT")
            

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw logo
        screen.blit(self.imageLogo, (self.rectLogo.x, self.rectLogo.y))

        if self.textWelcome:
            screen.blit(self.textWelcome, (250, 300))

        if self.createRoomButton:
            self.createRoomButton.draw(screen)

        if self.joinRoomButton:
            self.joinRoomButton.draw(screen)

        if self.textRoomCode:
            screen.blit(self.textRoomCode, (250, 360))

        if self.textRoomError:
            screen.blit(self.textRoomError, (250, 460))

        if self.roomCodeInputBox:
            self.roomCodeInputBox.draw(screen)

        if self.textNameInput:
            screen.blit(self.textNameInput, (300, 400))

        if self.nameInputErrorText:
            screen.blit(self.nameInputErrorText, (300, 490))

        if self.namaInputBox:
            self.namaInputBox.draw(screen)

        if self.nameSubmitButton:
            self.nameSubmitButton.draw(screen)
