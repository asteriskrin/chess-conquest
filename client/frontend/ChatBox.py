'''
Chat Box
'''

import pygame
from frontend.ChatInputBox import ChatInputBox
from frontend.Chat import Chat

class ChatBox:

    def __init__(self, onChatFunc):
        self.sound = pygame.mixer.Sound("frontend/music/done-for-you-612.wav")
        self.font = pygame.font.Font(None, 30)
        self.chatInputBox = ChatInputBox(650, 590, 280, 50)
        self.onChatFunc = onChatFunc
        self.chatHistory = []

    def handleEvent(self, event):
        message = self.chatInputBox.handleEvent(event)
        # If a message is entered
        if len(message) > 0:
            self.onChatFunc(message)

    def draw(self, screen):
        self.chatInputBox.draw(screen)
        # Render chat
        positionChat = 560
        for chat in reversed(self.chatHistory):
            chatString = chat.getPersonName() + ": " + chat.getMessage()
            renderChat = self.font.render(chatString, True, (255, 255, 255))
            screen.blit(renderChat, (650, positionChat))
            positionChat -= 30
            if positionChat < 200:
                break

    def addChat(self, personName, message):
        self.chatHistory.append(Chat(personName, message))
        self.sound.play()
