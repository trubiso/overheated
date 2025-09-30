import pygame

from engine import Engine, ObjectKind
from guljamonlib.pygame_controller import PygameController
from objects.background_controller import BackgroundController
from objects.player import Player
import sprites
from vector2 import Vector2
from objects.enemy import Enemy

SCREEN_SIZE = (640, 480)
engine = Engine(SCREEN_SIZE, PygameController(), 60)

def game(engine: Engine):
	background_controller = BackgroundController(sprites.PIXEL_PLATFORMER_BACKGROUNDS, 4, 2, 2, 1, Vector2(1, 0))
	enemy = Enemy(Vector2(20,40), Vector2(64, 64))

	engine.add_object(background_controller, ObjectKind.BACKGROUND)
	engine.add_object(Player(Vector2(23, 23), Vector2(64, 64)), ObjectKind.REGULAR)
	engine.add_object(enemy, ObjectKind.REGULAR)

engine.register("Game", game)
engine.switch_to("Game")

engine.run()
