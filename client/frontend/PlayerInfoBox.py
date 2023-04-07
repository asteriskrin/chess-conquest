'''
Player Info Box class
'''

from tkinter import Y
import pygame

class PlayerInfoBox:
    def __init__(self, x, y):
        self.baseFont = pygame.font.Font(None, 30)
        self.x = x
        self.y = y
        self.playerData = [["Jean", 3], ["Jean", 3], ["Jean", 3], ["Jack", 5]]

    '''
    Note:
    playerData is an Array 2D in format [Player Name, Amount of star].
    For example: playerData = [["Jean", 3], ["Jack", 5]]
    '''
    def setPlayerData(self, playerData):
        self.playerData = playerData

    def draw(self, screen):
        SPACER = 22
        textShow = self.baseFont.render("Star Point:", True, (255, 255, 255))
        screen.blit(textShow, (self.x, self.y))
        for i, player in enumerate(self.playerData):
            textString = "{}: {} star".format(player[0], player[1])
            textShow = self.baseFont.render(textString, True, (255, 255, 255))
            screen.blit(textShow, (self.x, self.y + (i+1)*SPACER))
