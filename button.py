import pygame

from settings import settings


class Button():
	def __init__(self, image, pos, textInput, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.textInput = textInput
		self.text = self.font.render(self.textInput, True, self.base_color)
		text_width = self.text.get_width()
		text_height = self.text.get_height()
		if self.image is None:
			self.image = self.text
		else:
			padded_width = int(text_width * 1.5)
			padded_height = int(text_height * 1.9)
			self.image = pygame.transform.scale(self.image, (padded_width, padded_height))
 
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.textInput, True, self.hovering_color)
		else:
			self.text = self.font.render(self.textInput, True, self.base_color)