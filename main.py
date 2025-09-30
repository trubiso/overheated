from engine import Engine, ObjectKind
import engine
from objects.background_controller import BackgroundController
from objects.player import Player
import sprites
from vector2 import Vector2
from objects.enemy import Enemy

def game(engine: Engine):
	background_controller = BackgroundController(sprites.PIXEL_PLATFORMER_BACKGROUNDS, 4, 2, 2, 1, Vector2(1, 0))
	enemy = Enemy(Vector2(20, 40), Vector2(64, 64))

	engine.add_object(background_controller, ObjectKind.BACKGROUND, "background_controller")
	engine.add_object(Player(Vector2(23, 23), Vector2(64, 64)), ObjectKind.REGULAR, "player")
	engine.add_object(enemy, ObjectKind.REGULAR, "enemy")

engine.engine.register("Game", game)
engine.engine.switch_to("Game")

engine.engine.run()
