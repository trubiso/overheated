import pygame
from hitbox import Hitbox
from object import Object
from tilemap import TileManager
from vector2 import Vector2


class BackgroundController(Object):
	def __init__(self, tile_manager: TileManager, i_start = 0, i_qty = 4, repeat_h = 1, repeat_v = 1, scroll = Vector2.zero(), scroll_freq = 10.0, j_start = 0, j_qty = 3):
		self.tile_size = 24
		self.tile_manager = tile_manager
		self.i_start = i_start
		self.i_qty = i_qty
		self.repeat_h = repeat_h
		self.repeat_v = repeat_v
		self.scroll = scroll
		self.scroll_freq = scroll_freq
		self.scrolls = scroll != Vector2.zero()
		self.j_start = j_start
		self.j_qty = j_qty
		self.surface = pygame.Surface((self.tile_size * i_qty * repeat_h, self.tile_size * j_qty * repeat_v))
		self.offset = Vector2.zero()
		self.scroll_ctr = 0
		self.position = Vector2.zero()
		self.hitbox = Hitbox(self.position, Vector2.zero())
	
	def draw(self, win: pygame.Surface):
		self.surface.fill(pygame.Color(0, 0, 0))

		for i in range(self.i_start, self.i_start + self.i_qty):
			for j in range(self.j_start, self.j_start + self.j_qty):
				tile = self.tile_manager.get_tile_at(i, j)
				for h in range(-1 if self.scrolls else 0, self.repeat_h + (1 if self.scrolls else 0)):
					for v in range(-1 if self.scrolls else 0, self.repeat_v + (1 if self.scrolls else 0)):
						self.surface.blit(tile, ((i - self.i_start + h * self.i_qty) * 24 + self.offset.x, (j - self.j_start + v * self.j_qty) * 24 + self.offset.y))
		
		pygame.transform.scale(self.surface, (640, 480), win)
	
	def update(self, _, dt):
		self.scroll_ctr += dt
		if self.scroll_ctr == self.scroll_freq:
			if self.scrolls:
				self.offset += self.scroll
				self.offset = self.offset.wrap(Vector2.zero(), Vector2(self.tile_size * self.i_qty, self.tile_size * self.j_qty))
			self.scroll_ctr = 0
