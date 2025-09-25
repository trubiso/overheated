from typing import Protocol
import pygame


class GameObject(Protocol):
	surface: pygame.Surface
	
	def draw(self, win: pygame.Surface):
		"""Draws the game object on a surface."""
	
	def update(self):
		"""Updates the game object."""
