'''
Name Input Box
'''

import pygame

class NameInputBox:
    COLOR_INACTIVE = (138, 138, 138)
    COLOR_ACTIVE = (255, 255, 255)
    def __init__(self, x, y, w, h, text = ""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(text, 1, self.color)
        self.active = False

    def getInput(self):
        return self.text

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active:
            self.color = self.COLOR_ACTIVE
        else:
            self.color = self.COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key != pygame.K_RETURN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = ""
                    else:
                        self.text += event.unicode
                self.text_surface = self.font.render(self.text, 1, self.color)

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
