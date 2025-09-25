from enum import Enum
from typing import Optional
import pygame
from guljamonlib.clock import Clock
from guljamonlib.controller import Controller
from object import Object


class ObjectKind(Enum):
	BACKGROUND = 1
	REGULAR = 2
	UI = 3

class Engine:
	def __init__(self, size: tuple[int, int], controller: Controller, fps = 30):
		global engine
		engine = self

		pygame.init()
		self.size = size
		self.screen = pygame.display.set_mode(size)
		self.controller = controller
		self.fps = fps
		self.background_objects: list[Object] = []
		self.objects: list[Object] = []
		self.ui_objects: list[Object] = []
		self.stages = {}
		self.current_stage = None
		pygame.display.set_caption("OVERHEATED")
	
	def add_object(self, game_object: Object, kind: ObjectKind):
		match kind:
			case ObjectKind.BACKGROUND:
				self.background_objects.append(game_object)
			case ObjectKind.REGULAR:
				self.objects.append(game_object)
			case ObjectKind.UI:
				self.ui_objects.append(game_object)
	
	def reset(self):
		self.background_objects = []
		self.objects = []
		self.ui_objects = []

	def register(self, stage_name, func):
		self.stages[stage_name] = func

	def switch_to(self, stage_name):
		self.reset()
		self.current_stage = stage_name
		func = self.stages[stage_name]
		print(f"Switching to {self.current_stage}")
		func(self)
	
	def run(self):
		clock = Clock(self.fps)
		delta_time = 1
		while not self.controller.shouldClose():
			self.controller.poll()
			self.update(delta_time)
			self.screen.fill(pygame.Color(0, 0, 0))
			self.draw()
			pygame.display.update()
			delta_time = clock.delay()
		pygame.quit()
	
	def update(self, dt):
		for game_object in self.background_objects + self.objects + self.ui_objects:
			game_object.update(self.controller, dt)

	def draw(self):
		for game_object in self.background_objects + self.objects + self.ui_objects:
			game_object.draw(self.screen)

engine: Optional[Engine] = None
