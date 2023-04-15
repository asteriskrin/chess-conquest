'''
Game Frontend class
'''

import pygame
from pygame import mixer
from frontend.ChessGameWindow import ChessGameWindow
from frontend.MainMenuWindow import MainMenuWindow

class GameFrontend:
    FPS_LIMIT = 30
    def __init__(self):
        pygame.init()
        mixer.init()
        self.bgm = None
        self.baseFont = pygame.font.Font(None, 24)
        self.WIN = pygame.display.set_mode((1000, 800))
        black = pygame.Color("Black")
        self.WIN.fill(black)
        pygame.display.set_caption('Chess Conquest')
        self.clock = pygame.time.Clock()

    def runLoop(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    if self.bgm:
                        self.bgm.stop()
                if self.window:
                    self.window.handleEvent(event)
            self.window.draw(self.WIN)
            self.clock.tick(self.FPS_LIMIT)
            pygame.display.flip()

    def stopLoop(self):
        self.run = False

    def getWin(self):
        return self.window

    def __attachWindow(self, window):
        self.window = window

    def openMainMenuWindow(self, callback1):
        if self.bgm:
            self.bgm.stop()
        self.bgm = pygame.mixer.Sound("frontend/music/MIRAI.ogg")
        self.bgm.play(loops=-1)
        mmw = MainMenuWindow(callback1)
        self.__attachWindow(mmw)

    def openChessGameWindow(self, callback1, callback2, callback3):
        if self.bgm:
            self.bgm.stop()

        self.bgm = pygame.mixer.Sound("frontend/music/Hello_my_world.ogg")
        self.bgm.play(loops=-1)
        self.__attachWindow(ChessGameWindow(callback1, callback2, callback3))
        return self.window
