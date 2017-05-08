import pygame
from pygame.locals import *
from spritesheet import *

class items():
    def __init__(self, gs, mode, imap, board):
        self.gs = gs
        self.mode = mode
        self.imap = imap
        self.board = board
        self.itemsList = list()

        self.itemDict = dict()
        self.itemDict[0]="NONE"
        self.itemDict[1]="PACDOT"
        self.itemDict[2]="POWERP"
        for i in range(len(self.imap)):
            temp = list()
            for j in range(len(self.imap[0])):
                tempItem = item(self.gs, self.board, self.itemDict[ self.imap[i][j] ], self.imap, j, i)
                temp.append(tempItem)
            self.itemsList.append(temp)
    def returnItemsList(self):
        return self.itemsList

class item(pygame.sprite.Sprite):
    def __init__(self, gs, board, iType, imap, posx, posy): 
        super(item, self).__init__()
        self.gs = gs
        self.board = board
        self.imap = imap
        self.iType = iType
        self.ss = spritesheet("pacman.sprite")
        self.posx = posx
        self.posy = posy
        self.black = (0,0,0)
        self.yratio = (self.board.rect.height - 34.0)/len(self.imap)
        self.xratio = (self.board.rect.width - 10)/len(self.imap[0])
        if(self.iType == "PACDOT"):
            self.image = self.ss.image_at((3, 81, 2, 2), colorkey = self.black)
        elif(self.iType == "POWERP"):
            self.image = self.ss.image_at((8,79,7,7), colorkey = self.black)
        elif(self.iType == "NONE"):
            self.image = self.ss.image_at((17,81,2,2), colorkey = self.black)

        self.rect = self.image.get_rect()
        w = round(self.rect.width*self.board.ratio)
        h = round(self.rect.height*self.board.ratio)

        self.image = pygame.transform.scale(self.image, (int(w), int(h)))

        self.baseX = self.board.rect.x + 10
        self.baseY = self.board.rect.y + 18

        self.rect.x = round(self.posx*self.xratio) + self.baseX + round(10-self.rect.width/2.0)
        self.rect.y = round(self.posy*self.yratio) + self.baseY + round(10-self.rect.height/2.0)

    def update(self):
        if(self.iType == "PACDOT"):
            self.image = self.ss.image_at((3, 81, 2, 2), colorkey = self.black)
        elif(self.iType == "POWERP"):
            self.image = self.ss.image_at((8,79,7,7), colorkey = self.black)
        elif(self.iType == "NONE"):
            self.image = self.ss.image_at((17,81,2,2), colorkey = self.black)

    def changeType(self, iType):
        self.iType = iType
