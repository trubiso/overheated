import pygame

from engine import Engine, ObjectKind
from guljamonlib.pygame_controller import PygameController
from objects.background_controller import BackgroundController
from objects.player import Player
import sprites
from vector2 import Vector2

SCREEN_SIZE = (640, 480)
engine = Engine(SCREEN_SIZE, PygameController(), 60)

def main_menu(engine: Engine):
	background_controller = BackgroundController(sprites.PIXEL_PLATFORMER_BACKGROUNDS, 4, 2, 2, 1, Vector2(1, 0))
	engine.add_object(background_controller, ObjectKind.BACKGROUND)
	engine.add_object(Player(Vector2(23, 23), Vector2(64, 64)), ObjectKind.REGULAR)

engine.register("Main Menu", main_menu)
engine.switch_to("Main Menu")

engine.run()
