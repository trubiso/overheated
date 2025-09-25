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
		# self.screen.blit(sprites.PIXEL_PLATFORMER_BACKGROUNDS.get_tile_at(4, 0), (0, 0))
		# self.screen.blit(sprites.PIXEL_PLATFORMER_BACKGROUNDS.get_tile_at(4, 1), (0, 24))
		# self.screen.blit(sprites.PIXEL_PLATFORMER_BACKGROUNDS.get_tile_at(4, 2), (0, 48))
		# self.screen.blit(sprites.PIXEL_PLATFORMER_BACKGROUNDS.get_tile_at(4, 3), (0, 24*3))

class BackgroundController(GameObject):
	def __init__(self, tile_manager: TileManager, i_start = 0, i_qty = 4, repeat_h = 1, repeat_v = 1, j_start = 0, j_qty = 3):
		self.tile_size = 24
		self.tile_manager = tile_manager
		self.i_start = i_start
		self.i_qty = i_qty
		self.repeat_h = repeat_h
		self.repeat_v = repeat_v
		self.j_start = j_start
		self.j_qty = j_qty
		self.surface = pygame.Surface((self.tile_size * i_qty * repeat_h, self.tile_size * j_qty * repeat_v))
	
	def draw(self, win: pygame.Surface):
		for i in range(self.i_start, self.i_start + self.i_qty):
			for j in range(self.j_start, self.j_start + self.j_qty):
				for h in range(self.repeat_h):
					for v in range(self.repeat_v):
						self.surface.blit(self.tile_manager.get_tile_at(i, j), ((i - self.i_start + h) * 24, (j - self.j_start + v) * 24))
		
		pygame.transform.scale(self.surface, (640, 480), win)

q = Vector2(3, 5)
t = Vector2(4, 9)
print((q + t).to_string())

class Enemy:
	def __init__(self, x, y, width, height, tileset, speed):
		pass

game = Game(640, 480, PygameController(), 60)
background_controller = BackgroundController(sprites.PIXEL_PLATFORMER_BACKGROUNDS, 4, 2, 2, 2)
game.add_game_object(background_controller)
game.run()
