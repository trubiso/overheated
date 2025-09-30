from object import KinematicObject
from vector2 import Vector2
import pygame
from tilemap import TileManager


class Enemy(KinematicObject):
	def __init__(self, position: Vector2, size: Vector2):
		super().__init__(position, size)
		self.base_speed = 1
		self.health = 3
		self.walk_count = 0
		sprite = pygame.image.load('sprites/pixel_platformer_pack/tiles/tile_0000.png')
		self.imagen = pygame.transform.scale(sprite, self.size.to_tuple())

	def draw(self, win: pygame.Surface):
		win.blit(self.imagen, (self.position.x, self.position.y, self.size.x, self.size.y))

	def move(self):
		pass

	def update(self, controller, dt):
		pass
