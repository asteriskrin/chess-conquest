'''
Start Button
'''

import pygame

class TextButton:
	def __init__(self, x, y, width, height, bgColor, bgHoverColor, textColor, text="Button", fontSize = 30):
		self.clickSound = pygame.mixer.Sound("frontend/music/glitchy-tone-97.wav")
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.bgColor = bgColor
		self.bgHoverColor = bgHoverColor
		self.textColor = textColor
		self.text = text

		self.rect = pygame.Rect(x, y, width, height)
		self.font = pygame.font.Font(None, fontSize)
		self.caption = self.font.render(text, 1, self.textColor)
		self.active = False

	def handleEvent(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.clickSound.play()
				print("TextButton clicked\n")
				return True
		return False

	def draw(self, screen):
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			pygame.draw.rect(screen, self.bgHoverColor, self.rect, 2)
		else:
			pygame.draw.rect(screen, self.bgColor, self.rect, 2)

		screen.blit(self.caption, (self.rect.x + 10, self.rect.y + 10))

		