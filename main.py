from typing import Protocol
import pygame
from guljamonlib.clock import Clock
from guljamonlib.controller import Controller
from guljamonlib.pygame_controller import PygameController
from object import GameObject
from tilemap import TileManager
from vector2 import Vector2
import sprites


class Game:
	def __init__(self, width: int, height: int, controller: Controller, fps = 30):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		self.controller = controller
		self.fps = fps
		self.game_objects: list[GameObject] = []
		pygame.display.set_caption("OVERHEATED")
	
	def add_game_object(self, game_object: GameObject):
		self.game_objects.append(game_object)
	
	def run(self):
		clock = Clock(self.fps)
		while not self.controller.shouldClose():
			self.controller.poll()
			self.update()
			self.screen.fill(pygame.Color(0, 0, 0))
			self.draw()
			pygame.display.update()
			clock.delay()
		pygame.quit()
	
	def update(self):
		for game_object in self.game_objects:
			game_object.update()

	def draw(self):
		for game_object in self.game_objects:
			game_object.draw(self.screen)
		# self.player.draw(self.screen)
		# self.enemy.draw(self.screen)

class BackgroundController(GameObject):
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
	
	def draw(self, win: pygame.Surface):
		self.surface.fill(pygame.Color(0, 0, 0))

		for i in range(self.i_start, self.i_start + self.i_qty):
			for j in range(self.j_start, self.j_start + self.j_qty):
				tile = self.tile_manager.get_tile_at(i, j)
				for h in range(-1 if self.scrolls else 0, self.repeat_h + (1 if self.scrolls else 0)):
					for v in range(-1 if self.scrolls else 0, self.repeat_v + (1 if self.scrolls else 0)):
						self.surface.blit(tile, ((i - self.i_start + h * self.i_qty) * 24 + self.offset.x, (j - self.j_start + v * self.j_qty) * 24 + self.offset.y))
		
		pygame.transform.scale(self.surface, (640, 480), win)
	
	def update(self):
		self.scroll_ctr += 1
		if self.scroll_ctr == self.scroll_freq:
			if self.scrolls:
				self.offset += self.scroll
				self.offset = self.offset.wrap(Vector2.zero(), Vector2(self.tile_size * self.i_qty, self.tile_size * self.j_qty))
			self.scroll_ctr = 0

# class player:

	
q = Vector2(3, 5)
t = Vector2(4, 9)
print((q + t).to_string())

# patata en sopa
class Enemy:
	def __init__(self, x, y, width, height, tileset, speed):
		pass

game = Game(640, 480, PygameController(), 60)
background_controller = BackgroundController(sprites.PIXEL_PLATFORMER_BACKGROUNDS, 4, 2, 2, 1, Vector2(1, 0))
game.add_game_object(background_controller)
game.run()
