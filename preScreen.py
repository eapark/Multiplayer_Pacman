import pygame
from pygame.locals import *


class preScreen(pygame.sprite.Sprite):
    def __init__(self, gs, text):
        self.myfont = pygame.font.SysFont("monospace", 18)
        self.gs = gs
        # render text
        self.image = self.myfont.render(text, 1, (255,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = round(self.gs.width/2.0 - self.rect.width/ 2.0)
        self.rect.y = round(self.gs.height/2.0 - self.rect.height/2.0)

    def update(self):
        pass
    
        

