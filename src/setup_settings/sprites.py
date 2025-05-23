import pygame
from .settings import * 

class Sprite(pygame.sprite.Sprite):
	def __init__(self, position, surface, groups):
		super().__init__(groups)
		self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
		self.image.fill('white')
		self.rect = self.image.get_rect(topleft = position)