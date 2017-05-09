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
        self.itemsCount = 0
        self.itemDict = dict()
        self.itemDict[0]="NONE"
        self.itemDict[1]="PACDOT"
        self.itemDict[2]="POWERP"
        self.images = dict()
        self.ss = spritesheet("pacman.sprite")
        self.black = (0,0,0)
        self.images["PACDOT"] = self.ss.image_at((3, 81, 2, 2), colorkey = self.black)
        self.images["POWERP"] = self.ss.image_at((8,79,7,7), colorkey = self.black)
        self.images["NONE"] = self.ss.image_at((17,81,2,2), colorkey = self.black)
        for key in self.images.keys():
                rect = self.images[key].get_rect()
                w = round(rect.width*self.board.ratio)
                h = round(rect.height*self.board.ratio)
                self.images[key] = pygame.transform.scale(self.images[key], (int(w), int(h)))
        for i in range(len(self.imap)):
            temp = list()
            for j in range(len(self.imap[0])):
                if(self.imap[i][j] != 0):
                    self.itemsCount += 1
                tempItem = item(self.gs, self.board, self.images, self.itemDict[ self.imap[i][j] ], self.imap, self, j, i)
                temp.append(tempItem)
            self.itemsList.append(temp)
    def getItemsList(self):
        return self.itemsList
    def decreaseItems(self):
        self.itemsCount -= 1
        if(self.itemsCount == 0):
            self.gs.pacmanWon()

class item(pygame.sprite.Sprite):
    def __init__(self, gs, board, images, iType, imap, parent, posx, posy): 
        super(item, self).__init__()
        self.gs = gs
        self.board = board
        self.imap = imap
        self.images = images
        self.iType = iType
        self.posx = posx
        self.posy = posy
        self.black = (0,0,0)
        self.parent = parent
        self.yratio = (self.board.rect.height - 34.0)/len(self.imap)
        self.xratio = (self.board.rect.width - 10)/len(self.imap[0])
        self.image = self.images[self.iType]
        self.rect = self.image.get_rect()
        
        self.baseX = self.board.rect.x + 10
        self.baseY = self.board.rect.y + 18

        self.rect.x = round(self.posx*self.xratio) + self.baseX + round(11-self.rect.width/2.0)
        self.rect.y = round(self.posy*self.yratio) + self.baseY + round(11-self.rect.height/2.0)
    def update(self):
        self.image = self.images[self.iType]
    def changeType(self, iType):
        self.iType = iType
    def collide(self):
        if(self.iType != "NONE"):
            self.iType = "NONE"
            self.parent.decreaseItems()
        
