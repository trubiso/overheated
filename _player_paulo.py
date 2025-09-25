# Player
# main.py
import pygame
import sys
import os
from random import randint

pygame.init()
WIDTH, HEIGHT = 1000, 600
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Background con suelo - Plataforma (demo)")
clock = pygame.time.Clock()

# Colores
SKY_TOP = (135, 206, 255)    # azul cielo claro
SKY_BOTTOM = (176, 226, 255) # azul más pálido
GROUND_COLOR = (100, 50, 20) # color base del suelo
TILE_COLOR = (150, 100, 50)  # color de las tejas/suelo

# Ground / tiles
TILE_WIDTH = 64
TILE_HEIGHT = 48
GROUND_Y = HEIGHT - 100  # y donde empieza el suelo (altura del suelo = HEIGHT - GROUND_Y)

# Cámara (simula desplazamiento horizontal)
camera_x = 0
camera_speed = 3
PLAYER_SPEED = 600  # px/s, velocidad horizontal del jugador

# Crear una superficie tileable para el suelo (puedes reemplazar por una imagen)
def create_tile_surface():
    surf = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
    surf.fill(TILE_COLOR)
    # dibujar detalle: líneas o piedras
    for i in range(3):
        pygame.draw.line(surf, (120, 80, 40), (0, TILE_HEIGHT//3 * i + 6), (TILE_WIDTH, TILE_HEIGHT//3 * i + 6), 2)
    # pequeña sombra en abajo
    pygame.draw.rect(surf, (90, 60, 30), (0, TILE_HEIGHT-8, TILE_WIDTH, 8))
    return surf

TILE_SURF = create_tile_surface()

# Nubes para parallax
class Cloud:
    def __init__(self):
        self.x = randint(0, WIDTH * 2)
        self.y = randint(20, HEIGHT // 3)
        self.scale = randint(60, 180) / 100.0
        self.speed = (1.0 / self.scale) * 0.5 + 0.2

    def update(self, dx):
        # dx: movimiento de la cámara
        self.x -= dx * (0.3 * (1/self.scale))  # parallax: objetos lejanos se mueven menos
        if self.x < -300:
            self.x = randint(WIDTH, WIDTH*2)
            self.y = randint(10, HEIGHT//3)

    def draw(self, surface):
        w = int(140 * self.scale)
        h = int(80 * self.scale)
        # simple forma de nube con círculos
        cloud_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(cloud_surf, (255,255,255,230), (0, h//4, w*0.8, h*0.6))
        pygame.draw.ellipse(cloud_surf, (255,255,255,230), (w*0.2, 0, w*0.8, h*0.7))
        surface.blit(cloud_surf, (self.x, self.y))

# Generar varias nubes
clouds = [Cloud() for _ in range(8)]

# Algunas plataformas elevadas (rects) para dar contexto
platforms = [
    pygame.Rect(200, GROUND_Y - 120, 160, 20),
    pygame.Rect(550, GROUND_Y - 200, 120, 20),
    pygame.Rect(900, GROUND_Y - 150, 200, 20),
    pygame.Rect(1400, GROUND_Y - 100, 180, 20),
]

# Función para pintar cielo con gradiente vertical
def draw_sky(surface):
    # gradiente simple
    for i in range(HEIGHT):
        t = i / HEIGHT
        r = int(SKY_TOP[0] * (1 - t) + SKY_BOTTOM[0] * t)
        g = int(SKY_TOP[1] * (1 - t) + SKY_BOTTOM[1] * t)
        b = int(SKY_TOP[2] * (1 - t) + SKY_BOTTOM[2] * t)
        pygame.draw.line(surface, (r,g,b), (0, i), (WIDTH, i))

# Dibujar suelo con tiles repetidos (infinite horizontal tiling)
def draw_ground(surface, camera_x):
    # dibujar base
    pygame.draw.rect(surface, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

    # determinar cuál tile inicio y cuántas tiles dibujar
    start_tile = int((camera_x) // TILE_WIDTH) - 2
    num_tiles = WIDTH // TILE_WIDTH + 6

    for i in range(start_tile, start_tile + num_tiles):
        x = i * TILE_WIDTH - camera_x
        # jitter vertical o variación si quieres
        surface.blit(TILE_SURF, (x, GROUND_Y))

    # sombra sobre el borde del suelo
    pygame.draw.rect(surface, (0,0,0,40), (0, GROUND_Y, WIDTH, 8), border_radius=0)

# Dibujar plataformas (rects) con offset de cámara
def draw_platforms(surface, camera_x):
    for rect in platforms:
        r = rect.copy()
        r.x -= camera_x
        pygame.draw.rect(surface, (180,140,90), r)
        pygame.draw.rect(surface, (140,100,60), r, 4)

bullet_group = pygame.sprite.Group()

# loop principal
def main():
    global camera_x
    # crear player una vez (coordenadas en el mundo)
    player = Player(100, GROUND_Y - 50, 30, 50, bullet_group)
    last_jump_pressed = False

    running = True
    prev_camera_x = camera_x
    while running:
        dt = clock.tick(FPS) / 1000.0

        # ---- eventos ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # control: mover al jugador con izq/der
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left(PLAYER_SPEED)
        elif keys[pygame.K_RIGHT]:
            player.move_right(PLAYER_SPEED)
        else:
            player.x_vel = 0

        # manejar salto por borde (solo en la transición de no presionado->presionado)
        jump_pressed = (keys[pygame.K_SPACE] or keys[pygame.K_UP])
        if jump_pressed and not last_jump_pressed:
            # primer salto si estamos en suelo
            if player.on_ground:
                player.try_jump()
            else:
                # doble salto: sólo si no lo hemos usado ya y estamos cayendo
                player.double_jump()
        last_jump_pressed = jump_pressed

        # disparar
        shots_fired = (keys[pygame.KSCAN_F])
        if shots_fired:
            player.shoot()


        # calcular cámara para seguir al jugador (centrado)
        # la cámara está en coordenadas del mundo; la centramos en el jugador
        camera_x = max(0, player.rect.centerx - WIDTH // 2)
        dx = camera_x - prev_camera_x

        # ---- actualizar nubes (parallax) ----
        for c in clouds:
            c.update(dx)

        # actualizar player (física y colisiones)
        player.update(dt, platforms)

        # actualizar balas (movimiento y recogida)
        bullet_group.update()

     

        prev_camera_x = camera_x

        # ---- dibujado ----
        draw_sky(WIN)

        # dibujar nubes (colócalas antes del ground para parallax/ profundidad)
        for c in clouds:
            c.draw(WIN)

        # dibujar plataformas (con offset)
        draw_platforms(WIN, camera_x)

        # dibujar suelo tiled
        draw_ground(WIN, camera_x)

        # dibujar player restando el offset de la cámara
        player.draw(WIN, camera_x)

        # dibujar balas (con offset de cámara)
        for b in bullet_group:
            br = b.rect.copy()
            br.x -= camera_x
            WIN.blit(b.image, br)

        # HUD pequeño
        font = pygame.font.SysFont(None, 20)
        txt = font.render("Usa izq/der para mover la cámara, SPACE/UP para saltar", True, (0,0,0))
        WIN.blit(txt, (8, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height, bullet_group):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0   
        self.on_ground = False
        self.has_double_jumped = False
        self.bullet_group = bullet_group

    def move(self, dx, dy):
        self.rect.x += dx 
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right(self, vel):
        self.x_vel = vel 
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def jump(self, vel):
        # impulso vertical inmediato (vel > 0)
        self.y_vel = -vel
        if self.direction != "jump":
            self.direction = "jump"
            self.animation_count = 0

    def try_jump(self, vel = 700):
        # sólo saltar si estamos en el suelo
        if self.on_ground:
            self.jump(vel)
            self.on_ground = False
            # permitir doble salto después de despegar
            self.has_double_jumped = False
    
    def double_jump(self, vel = 500):
        # sólo permitir un doble salto mientras estemos en aire y no lo hayamos usado
        if (not self.on_ground) and (not self.has_double_jumped):
            if self.y_vel > 0:
                self.jump(vel)
                self.has_double_jumped = True
    
    def shoot(self):
        # crear una bala en la posición del jugador
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        
    def update(self, dt, platforms):
        # Física simple: gravedad, movimiento y colisiones con suelo/plataformas
        GRAVITY = 2000  # pixels / s^2

        # aplicar gravedad
        self.y_vel += GRAVITY * dt 

        # aplicar movimiento horizontal (si se quiere más adelante)
        self.rect.x += int(self.x_vel * dt)

        # mover verticalmente
        self.rect.y += int(self.y_vel * dt)

        # resetear bandera de suelo
        self.on_ground = False

        # colisión con plataformas (comprobación simple desde arriba)
        for plat in platforms:
            # comprobamos si estamos cayendo y colisionamos con la plataforma
            if self.rect.colliderect(plat):
                # sólo hacemos corrección si venimos desde arriba
                if self.y_vel >= 0 and (self.rect.bottom - self.y_vel * dt) <= plat.top:
                    self.rect.bottom = plat.top
                    self.y_vel = 0
                    self.on_ground = True
                    # reset double-jump availability when we land
                    self.has_double_jumped = False

        # colisión con suelo (GROUND_Y)
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.y_vel = 0
            self.on_ground = True
            # reset double-jump availability when we land on ground
            self.has_double_jumped = False
    
    def draw(self, win):
        # compat: draw(world_position - camera_x)
        # if caller passes camera offset, handle it
        try:
            # draw signature draw(win, camera_x)
            raise Exception
        except Exception:
            # fallback if called with one arg (legacy)
            pygame.draw.rect(win, self.COLOR, self.rect)

    def draw(self, win, camera_x=0):
        r = self.rect.copy()
        r.x -= camera_x
        pygame.draw.rect(win, self.COLOR, r)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group, player):
        super().__init__()

        # velocidad de las balas (px per frame; can be adjusted)
        self.velocity = 20
        self.range = 450  # Pixeles antes que la bala desaparezca

        # Determine facing: prefer explicit player.direction, fallback to x_vel
        facing_right = False
        if hasattr(player, 'direction') and player.direction in ("left", "right"):
            facing_right = (player.direction == "right")
        else:
            facing_right = getattr(player, 'x_vel', 0) > 0

        # Try to load bullet image from likely locations relative to this file
        base_dir = os.path.dirname(__file__)
        candidates = [
            os.path.join(base_dir, 'sprites', 'bullet.png'),
            os.path.join(base_dir, 'gamesprites', 'bullet.png'),
            os.path.join(base_dir, '..', 'sprites', 'bullet.png'),
        ]

        found = None
        for p in candidates:
            if os.path.exists(p):
                found = p
                break

        if found:
            bullet_img = pygame.image.load(found)
            bullet_img = pygame.transform.scale(bullet_img, (30, 14))
        else:
            print(f"Warning: bullet sprite not found. Tried: {candidates}. Using placeholder.")
            bullet_img = pygame.Surface((30, 14), pygame.SRCALPHA)
            bullet_img.fill((255, 200, 0))
            pygame.draw.rect(bullet_img, (0, 0, 0), bullet_img.get_rect(), 2)

        if facing_right:
            self.image = bullet_img
        else:
            self.image = pygame.transform.flip(bullet_img, True, False)
            self.velocity = -abs(self.velocity)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.starting_x = x

        bullet_group.add(self)

    def update(self):
        self.rect.x += self.velocity

        # Eliminar la bala si ha recorrido su rango
        if abs(self.rect.x - self.starting_x) > self.range:
            self.kill()

bullet_group = pygame.sprite.Group()
bullet_group.update()
bullet_group.draw(WIN)
if __name__ == "__main__":
    main()