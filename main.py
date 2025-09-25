from typing import Protocol
import pygame, sys, os
from os import listdir
from os.path import isfile, join 
from guljamonlib.clock import Clock
from guljamonlib.controller import Controller
from guljamonlib.pygame_controller import PygameController
from object import GameObject
from tilemap import TileManager
from vector2 import Vector2
import sprites




UP = 2
DOWN = 0
HORIZONTAL = 1
ANIMATION_FRAME_RATE = 10
WINDOW = pygame.display.set_mode((640, 480))

CLOCK = pygame.time.Clock()

objects = []
enemies =[]

class Game:
	def __init__(self, controller):
		pygame.init()
		self.controller = controller
		self.game_objects: list[GameObject] = []
		pygame.display.set_caption("OVERHEATED")
	
	def add_game_object(self, game_object: GameObject):
		self.game_objects.append(game_object)
	
	def run(self):
		CLOCK.tick(60)
		while not self.controller.shouldClose():
			self.controller.poll()
			self.update()
			self.screen.fill(pygame.Color(0, 0, 0))
			self.draw()
			pygame.display.update()
			CLOCK.delay()
		pygame.quit()
	
	def update(self):
		for game_object in self.game_objects:
			game_object.update()


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

class Enemy:
	def __init__(self, x, y, width, height, tileset, speed):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.tileset = tileset 
		self.speed = speed
		self.health = 3
		self.flipX = False

		enemies.append(self)

	def draw(self):
		image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction],(self.width,self.height))

		self.change_direction()

		image = pygame.transform.flip(image,self.flipX, False)
		WINDOW.blit(image, (self.x, self.y))

		if self.velocity[0] == 0 and self.velocity[1] == 0:
			self.frame = 0
			return
		
		self.frame_timer +=1

		if self.frame_timer < ANIMATION_FRAME_RATE:
			return
		
		self.frame +=1
		if self.frame >= len(self.frames):
			self.frame = 0

		self.frame_timer = 0

	def update(self):
		player_center = player.get_center()
		enemy_center = self.get_center()

		self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]

		magnitude = (self.velocity[0] ** 2 +self.velocity[1] ** 2) ** 0.5

		self.velocity = [self.velocity[0] / magnitude*self.speed, self.velocity[1] / magnitude*self.speed] 

		self.x += self.velocity[0] *self.speed
		self.y += self.velocity[1] *self.speed
		self.draw()

	

	def change_direction(self):
		if self.velocity[0] < 0:
			self.direction = HORIZONTAL
			self.flipX = True
		elif self.velocity[0]>0:
			self.direction = HORIZONTAL
			self.flipX = False
		elif self.velocity[1] > 0:
			self.direction = DOWN
		elif self.velocity[1] < 0:
			self.direction = UP

		if self.velocity[1] > self.velocity[0]>0:
			self.direction = DOWN
		elif self.velocity[1] < self.velocity[0]<0:
			self.direction = UP

	def take_damage(self, damage):
		self.health -= damage
		if self.health <= 0:
			self.destroy()


	def destroy(self):
		objects.remove(self)
		enemies.remove(self)


def load_tileset(filename, width,height):
	image = pygame.image.load(filename).convert_alpha()
	image_width, image_height = image.get_size()
	tileset = []
	for tile_x in range(0, image_width // width):
		line = []
		tileset.append(line)
		for tile_y in range(0, image_height // height):
			rect = (tile_x * width, tile_y * height, width, height)
			line.append(image.subsurface(rect))
	return tileset

player = None
enemy = Enemy(200,200, 75, 75, "sprites/pixel_platformer_pack/tiles/characters/tile_0000.png" , 5)

		
		

game = Game  (PygameController())
background_controller = BackgroundController(sprites.PIXEL_PLATFORMER_BACKGROUNDS, 4, 2, 2, 2)
game.add_game_object(background_controller)
game.run()







