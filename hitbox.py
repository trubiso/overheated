from typing import Tuple
from vector2 import Vector2


class Hitbox:
	def __init__(self, position: Vector2, size: Vector2):
		self.l1 = position
		self.l2 = position + Vector2(0, size.y)
		self.r1 = position + Vector2(size.x, 0)
		self.r2 = position + size

	def to_tuple(self) -> Tuple[Vector2, Vector2, Vector2, Vector2]:
		return self.l1, self.l2, self.r1, self.r2

	def to_string(self):
		return f"[l1: {self.l1.to_string()}, l2: {self.l2.to_string()}," \
				f"r1: {self.r1.to_string()}, r2: {self.r2.to_string()}]"

	def collides_horizontally(self, hitbox2):
		if hitbox2.l1.x < self.l1.x < hitbox2.r2.x:
			return True
		if hitbox2.l1.x < self.r2.x < hitbox2.r2.x:
			return True
		if self.l1.x <= hitbox2.l1.x and self.r2.x >= hitbox2.r2.x:
			return True
		if hitbox2.l1.x <= self.l1.x and hitbox2.r2.x >= self.r2.x:
			return True
		return False

	def collides_vertically(self, hitbox2):
		if hitbox2.l1.y < self.l1.y < hitbox2.r2.y:
			return True
		if hitbox2.l1.y < self.r2.y < hitbox2.r2.y:
			return True
		if self.l1.y <= hitbox2.l1.y and self.r2.y >= hitbox2.r2.y:
			return True
		if hitbox2.l1.y <= self.l1.y and hitbox2.r2.y >= self.r2.y:
			return True
		return False

	def collides_with(self, other):
		if self.collides_horizontally(other) and self.collides_vertically(other):
			return True
		return False
