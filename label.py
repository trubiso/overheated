import pygame

fonts = {}
labels = []

anti_alias = True
font_folder_path = "OVERHEATED/fonts"

class Label:
    def __init__(self,font,text,size=32,color=(255,255,255)):
        global labels
        self.color = color
        if font in fonts:
            self.font = fonts[font]
        else:
            self.font = pygame.font.Font(font_folder_path + "/" + font, size)
        self.set_text(text)
        labels.append(self)

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.color)

    def draw (self, screen):
        screen.blit(self.surface,(self.entity.x, self.entity.y))