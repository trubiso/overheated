from typing import Protocol
import pygame
from guljamonlib.controller import Controller
from hitbox import Hitbox
from vector2 import Vector2


class Object(Protocol):
	surface: pygame.Surface
	position: Vector2
	hitbox: Hitbox
	
	def draw(self, win: pygame.Surface):
		"""Draws the game object on a surface."""
	
	def update(self, controller: Controller, dt: float):
		"""Updates the game object."""

class KinematicObject(Object):
	def __init__(self, position: Vector2, size: Vector2 = Vector2(32, 32)):
		self.position: Vector2 = position
		self.speeds: Vector2 = Vector2(0, 0)
		self.size: Vector2 = size
		self.hitbox = Hitbox(self.position, self.size)
		self.surface = pygame.Surface(self.size.to_tuple())

	def update_hitbox(self):
		self.hitbox = Hitbox(self.position, self.size)

	def move_position_x(self, diff: float):
		self.position.x += diff
		self.update_hitbox()

	def move_position_y(self, diff: float):
		self.position.y += diff
		self.update_hitbox()

	def apply_speed_x(self, dt=1.0):
		self.move_position_x(self.speeds.x * dt)

	def apply_speed_y(self, dt=1.0):
		self.move_position_y(self.speeds.y * dt)
