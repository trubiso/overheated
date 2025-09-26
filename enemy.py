from object import KinematicObject
from vector2 import Vector2
import pygame
from tilemap import TileManager


class Enemy(KinematicObject):

    walk = pygame.image.load('sprites/pixel_platformer_pack/tiles/tile_0000.png')
    def __init__(self, position: Vector2, size: Vector2, imagen: TileManager):
        super().__init__(position, size = Vector2.from_tuple(size.get_size()))
        self.base_speed = 1
        self.health = 3
        self.walk_count = 0
        self.imagen = imagen

        
    def draw(self, win: pygame.Surface):
        win.fill((27, 60, 253), (self.position.x, self.position.y, self.size.x, self.size.y))

    def move(self):
        pass

    def update(self, controller, dt):
        pass
    


		