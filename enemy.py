from object import KinematicObject
from vector2 import Vector2
import pygame


class Enemy(KinematicObject):

    walk = pygame.image.load('sprites/pixel_platformer_pack/tiles/tile_0000.png')
    def __init__(self, position: Vector2, imagen: pygame.Surface):
        super().__init__(position, Vector2.from_tuple(imagen.get_size()))
        self.base_speed = 1
        self.imagen = imagen
        self.health = 3
        self.walk_count = 0

        
    def draw(self, win):
        self.move()
        if self.walk_count + 1 >= 33:
            self.walk_count = 0

        if self.base_speed>0:
            win.blit(self.walk[self.walk_count//3],(self.position))
            self.walk_count += 1
        else:
            win.blit(self.walk[self.walk_count//3],(self.position))
            self.walk_count += 1

    def move(self):
        pass

    def update(self):
        pass
    


		