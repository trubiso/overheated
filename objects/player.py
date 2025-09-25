import pygame
from guljamonlib.controller import ButtonKind, Controller
from object import KinematicObject
from utils import lerp
from vector2 import Vector2


class Player(KinematicObject):
	def __init__(self, position: Vector2, size: Vector2):
		super().__init__(position, size)
		self.base_speed = 4000
		self.jump_speed = 8000
		self.gravity = 200000
		self.lerp_strength = 0.8
	
	def draw(self, win: pygame.Surface):
		win.fill((23, 19, 213), (self.position.x, self.position.y, self.size.x, self.size.y))
	
	def update(self, controller: Controller, dt: float):
		self.speeds.x = lerp(self.speeds.x, (controller.isPressed(ButtonKind.Right) - controller.isPressed(ButtonKind.Left)) * self.base_speed, self.lerp_strength)
		self.speeds.y += self.gravity * dt
		if controller.isShortPressed(ButtonKind.A):
			self.speeds.y = -self.jump_speed
		
		self.apply_speed_x(dt)
		self.apply_speed_y(dt)

		if self.position.y > 480 - self.size.y:
			self.position.y = 480 - self.size.y
			self.speeds.y = 0

        # TODO: cambiar el lerp en el aire para que no puedas moverte tanto en él