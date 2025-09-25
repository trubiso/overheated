from typing import Self
from utils import clamp, lerp, wrap

class Vector2:
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y
	
	def __eq__(self, value: Self) -> bool:
		return self.x == value.x and self.y == value.y
	
	def __neg__(self):
		return Vector2(-self.x, -self.y)
	
	def __add__(self, value: Self):
		return Vector2(self.x + value.x, self.y + value.y)
	
	def __sub__(self, value: Self):
		return self + -value
	
	def to_string(self):
		return f"({self.x}, {self.y})"
	
	def clamp(self, min: Self, max: Self):
		return Vector2(clamp(self.x, min.x, max.x), clamp(self.y, min.y, max.y))
	
	def wrap(self, min: Self, max: Self):
		return Vector2(wrap(self.x, min.x, max.x), wrap(self.y, min.y, max.y))

	def lerp(self, destination: Self, strength: float):
		self.x = lerp(self.x, destination.x, strength)
		self.y = lerp(self.y, destination.y, strength)
	
	@staticmethod
	def zero():
		return Vector2(0, 0)