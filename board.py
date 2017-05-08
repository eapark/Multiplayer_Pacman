import pygame
from pygame.locals import *
from spritesheet import spritesheet

class board(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.gs = gs
        super(board, self).__init__()
        self.ss = spritesheet("pacman.sprite")
        self.image = self.ss.image_at((371,4,164,212), colorkey=(0,0,0))
        self.rect = self.image.get_rect()
        self.originalHeight = self.rect.height
        self.ratio = self.gs.height/float(self.rect.height)

        self.rect.height = round(self.rect.height*self.ratio - 10)
        self.ratio = self.rect.height/self.originalHeight
        self.rect.width = round(self.rect.width*self.ratio)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        
        self.rect.x = round((self.gs.width - self.rect.width)/2)
        self.rect.y = round((self.gs.height - self.rect.height)/2)
        print("self.rect is", self.rect)

    def update(self):
        pass
