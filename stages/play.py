import pygame

pygame.init()

# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WINDOW_SIZE = (1280, 720)
WINDOW_TITLE = "Pygame Tutorial"


HORIZONTAL = 1
UP = 2
DOWN = 0

FRAME_RATE = 60
ANIMATION_FRAME_RATE = 10

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

CLOCK = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("sprites/pixel_platformer_pack/tiles/characters/tile_0003.png"), WINDOW_SIZE)

objects = []
bullets = []
enemies = []


class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]
        self.collider = [width, height]

        objects.append(self)

    def draw(self):
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2


class Entity(Object):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, None)
        self.speed = speed

        self.tileset = load_tileset(tileset, 16, 16)
        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0, 1, 0, 2]
        self.frame_timer = 0

    def change_direction(self):
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipX = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipX = False
        elif self.velocity[1] > 0:
            self.direction = DOWN
        elif self.velocity[1] < 0:
            self.direction = UP

    def draw(self):
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction],(self.width,self.height))

        self.change_direction()

        image = pygame.transform.flip(image, self.flipX, False)
        WINDOW.blit(image, (self.x, self.y))

        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0
            return

        self.frame_timer += 1

        if self.frame_timer < ANIMATION_FRAME_RATE:
            return

        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0

        self.frame_timer = 0

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()


class Player(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)

    def update(self):
        super().update()


class Enemy(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)

        self.health = 3
        self.collider = [width / 2.5, height / 1.5]
        enemies.append(self)

    def update(self):
        player_center = player.get_center()
        enemy_center = self.get_center()

        self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]

        magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        self.velocity = [self.velocity[0] / magnitude * self.speed, self.velocity[1] / magnitude * self.speed]

        super().update()

    def change_direction(self):
        super().change_direction()

        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] < 0:
            self.direction = UP

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        objects.remove(self)
        enemies.remove(self)


def check_input(key, value):
    if key == pygame.K_LEFT or key == pygame.K_a:
        player_input["left"] = value
    elif key == pygame.K_RIGHT or key == pygame.K_d:
        player_input["right"] = value
    elif key == pygame.K_UP or key == pygame.K_w:
        player_input["up"] = value
    elif key == pygame.K_DOWN or key == pygame.K_s:
        player_input["down"] = value


def load_tileset(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0, image_width // width):
        line = []
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset


player_input = {"left": False, "right": False, "up": False, "down": False}

# Objects
player = Player(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, 75, 75, "sprites/pixel_platformer_pack/tiles/characters/tile_0006.png", 5)
target = Object(0, 0, 50, 50, pygame.image.load("sprites/pixel_platformer_pack/tiles/characters/tile_0005.png"))
enemy = Enemy(200, 200, 75, 75, "sprites/pixel_platformer_pack/tiles/characters/tile_0000.png", 2)

pygame.mouse.set_visible(False)


def shoot():
    player_center = player.get_center()
    bullet = Object(player_center[0], player_center[1], 16, 16, pygame.image.load("assets/bullet.png"))

    target_center = target.get_center()
    bullet.velocity = [target_center[0] - player_center[0], target_center[1] - player_center[1]]

    magnitude = (bullet.velocity[0] ** 2 + bullet.velocity[1] ** 2) ** 0.5

    bullet.velocity = [bullet.velocity[0] / magnitude * 10, bullet.velocity[1] / magnitude * 10]

    bullets.append(bullet)


def check_collisions(obj1, obj2):
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()
    w1, h1 = obj1.collider[0] / 2, obj1.collider[1] / 2
    w2, h2 = obj2.collider[0] / 2, obj2.collider[1] / 2
    if x1 + w1 > x2 - w2 and x1 - w1 < x2 + w2:
        return y1 + h1 > y2 - h2 and y1 - h1 < y2 + h2
    return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            check_input(event.key, True)
        elif event.type == pygame.KEYUP:
            check_input(event.key, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot()

    mousePos = pygame.mouse.get_pos()
    target.x = mousePos[0] - target.width / 2
    target.y = mousePos[1] - target.height / 2

    player.velocity[0] = player_input["right"] - player_input["left"]
    player.velocity[1] = player_input["down"] - player_input["up"]

    WINDOW.blit(background, (0, 0))

    for obj in objects:
        obj.update()

    for b in bullets:
        if BOUNDS_X[0] <= b.x <= BOUNDS_X[1] and BOUNDS_Y[0] <= b.y <= BOUNDS_Y[1]:
            continue
        bullets.remove(b)
        objects.remove(b)

    for e in enemies:
        for b in bullets:
            if check_collisions(b, e):
                e.take_damage(1)
                bullets.remove(b)
                objects.remove(b)

    CLOCK.tick(FRAME_RATE)
    pygame.display.update()





