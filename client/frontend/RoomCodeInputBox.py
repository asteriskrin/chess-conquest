'''
Room Code Input Box
'''

import pygame


class RoomCodeInputBox:
    COLOR_INACTIVE = (138, 138, 138)
    COLOR_ACTIVE = (255, 255, 255)
    VALID_KEYPRESS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.roomCode = ""
        self.font = pygame.font.Font(None, 60)
        self.textSurface = self.font.render(self.roomCode, 1, self.color)
        self.active = False

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
                if event.key == pygame.K_BACKSPACE:
                    if len(self.roomCode) > 0:
                        self.roomCode = self.roomCode[0:len(self.roomCode)-1]
                elif event.key in self.VALID_KEYPRESS:
                    if len(self.roomCode) < 6:
                        self.roomCode += event.unicode
                self.textSurface = self.font.render(self.roomCode, 1, self.color)

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, self.COLOR_ACTIVE, self.rect, 2)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 2)
    
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))

    def getRoomCode(self):
        if not self.roomCode: return int(0)
        return int(self.roomCode)
