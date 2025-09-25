from object import KinematicObject
from vector2 import Vector2
import pygame


class Enemy(KinematicObject):
    def __init__(self, position: Vector2, imagen: pygame.Surface):
        super().__init__(position, Vector2.from_tuple(imagen.get_size()))
        self.base_speed = 1
        self.imagen = imagen
        self.health = 3
        self.walk_count = 0

        
    def draw(self, win):
        self.move()
        if self.walk_count + 1 >= 33:
            pass

    def move(self):
        pass

    def update(self):
        pass
    


		