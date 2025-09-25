import pygame
pygame.init()

engine = None
deafult_width = 640
deafult_height = 480

keys_down = set()
import pygame

def key_pressed(key):
    return key in keys_down

def mouse_pressed(button):
    return pygame.mouse.get_pressed()[button]

class Engine:
            
    def __init__(self):
        global engine
        engine = self

        self.active_objs = []

        self.background_drawables = [] # backgrounds
        self.drawables = [] #drawn in the world
        self.ui_drawables = [] # drawn ui

        self.clear_color = (30,150,240)

        self.screen = self.create_screen()

        self.stages = {}
        self.current_stage = None

    def create_screen(self):
        pygame.display.set_caption("OVERHEATED")

        screen = pygame.display.set_mode((620,480))

    def register(self, stage_name, func):
        self.stages[stage_name] = func


    def switch_to(self,stage_name):
        self.reset()
        self.current_stage = stage_name
        func = self.stages [stage_name]
        print(f"Switching to {self.current_stage}") # for debug
        func()

    def run(self):
        from input import keys_down

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                elif event.type == pygame.KEYUP:
                    keys_down.remove(event.key)

            for a in self.active_objs:
                a.update()

            pygame.display.get_surface().fill(self.clear_color)

            for b in self.background_drawables:
                b.draw(self.screen)

            for s in self.drawables:
                s.draw(self.screen)

            for l in self.ui_drawables:
                l.draw(self.screen)

            pygame.display.flip()

            pygame.time.delay(17)

        pygame.quit()



    def reset(self):
        pass

