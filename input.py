#to track what key is down
keys_down = set()
import pygame

def key_pressed(key):
    return key in keys_down

def mouse_pressed(button):
    return pygame.mouse.get_pressed()[button]