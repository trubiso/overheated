from vector2 import Vector2
import pygame


class TileManager:
	def __init__(self, filename: str, tile_size: Vector2, offset: Vector2, columns: int, rows: int, color_key = None):
		if not pygame.get_init():
			pygame.init()

		self.sheet = pygame.image.load(filename)
		self.tile_size = tile_size
		self.offset = offset
		self.columns = columns
		self.rows = rows
		strips = [self.load_strip(row, self.columns, color_key) for row in range(self.rows)]
		self.tiles = [i for s in strips for i in s]

	def get_tile(self, num: int) -> pygame.Surface:
		return self.tiles[num]

	def get_tile_at(self, col: int, row: int) -> pygame.Surface:
		return self.get_tile(col + row * self.columns)
		
	def image_at(self, rectangle, color_key) -> pygame.Surface:
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size)
		image.blit(self.sheet, (0, 0), rect)
		if color_key is not None:
			if color_key == -1:
				color_key = image.get_at((0, 0))
			image.set_colorkey(color_key, pygame.RLEACCEL)
		return image

	def images_at(self, rects, color_key) -> list[pygame.Surface]:
		return [self.image_at(rect, color_key) for rect in rects]

	def load_strip(self, row: int, image_count: int, color_key=None) -> list[pygame.Surface]:
		return self.images_at([(self.tile_size.x * x + self.offset.x, row * self.tile_size.y + self.offset.y, self.tile_size.x, self.tile_size.y)
		                      for x in range(image_count)], color_key)