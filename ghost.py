import pygame
from pygame.locals import *
from spritesheet import *

class ghost(pygame.sprite.Sprite):
    def __init__(self, gs, mode, gmap, board, color):
        super(ghost, self).__init__()
        self.gs = gs
        self.mode = mode
        self.gmap = gmap
        self.board = board
        self.color = color
        self.yratio = (self.board.rect.height - 34.0)/len(self.gmap)
        self.xratio = (self.board.rect.width -10)/len(self.gmap[0])
        self.stuck = False
        self.spritefile = "pacman.sprite"
        ss = spritesheet(self.spritefile)
        self.black = (0,0,0)
        self.ghostImages = dict()
        # Below we load a sprite twice to keep the order in which it moves. We sacrifice memory for easier coding
        if(color == "RED"):
            iBaseY = 0;
        elif(color == "PINK"):
            iBaseY = 18;
        elif(color == "CYAN"):
            iBaseY = 36;
        elif(color == "ORANGE"):
            iBaseY = 54;
        else:
            raise Exception("Not a proper color")

        self.ghostImages["RIGHT"] = ss.images_at(((3, 125+iBaseY, 14, 13), (20, 125+iBaseY, 14, 13), (3, 125+iBaseY, 14, 13), (20, 125+iBaseY, 14, 13)), colorkey=self.black)
        self.ghostImages["LEFT"]  = ss.images_at(((37, 125+iBaseY, 14, 13), (54,125+iBaseY,14,13),(37,125+iBaseY,14,13),(54,125+iBaseY,14,13)), colorkey=self.black)
        self.ghostImages["UP"]    = ss.images_at(((71,125+iBaseY,14,13), (88,125+iBaseY,14,13),(71,125+iBaseY,14,13),(88,125+iBaseY,14,13)), colorkey=self.black)
        self.ghostImages["DOWN"]  = ss.images_at(((105,125+iBaseY,14,13),(122,125+iBaseY,14,13),(105,125+iBaseY,14,13),(122,125+iBaseY,14,13)),colorkey=self.black)
        
        self.ghostSpooked = dict()
        self.ghostSpooked["V1"]   = ss.images_at(((3,197,14,13),(20,197,14,13),(3,197,14,13),(20,197,14,13)),colorkey=self.black) # Just blue
        self.ghostSpooked["V2"]   = ss.images_at(((3,197,14,13),(20,197,14,13),(37,197,14,13),(54,197,14,13)),colorkey=self.black) # Flicker between blue and white

        # Scale images
        for key, imageL in self.ghostImages.iteritems():
            for n in range(4):
                rect = imageL[n].get_rect()
                w = round(rect.width*self.board.ratio*0.8)
                h = round(rect.height*self.board.ratio*0.8)
                imageL[n] = pygame.transform.scale(imageL[n], (int(w), int(h)))
        
        self.moving = True
        self.spooked = False
        self.trapped = True # Inside the middle room
        self.rect = [0,0,0,0]
        self.innerTick = 0
        self.posx = 9
        self.posy = 11
        self.baseX = self.board.rect.x + 10
        self.baseY = self.board.rect.y + 18
        self.boardMaxY = len(self.gmap)
        self.boardMaxX = len(self.gmap[0])
        self.movingDirection = "RIGHT"
        self.setDirection = "RIGHT"
        self.iter = 0
        self.image = self.ghostImages[self.movingDirection][1]
        self.toTick = True
    def calcRect(self):
        self.rect = self.image.get_rect()
        xoffset = 0
        yoffset = 0
        if(self.movingDirection == "RIGHT"):
            xoffset = round(self.innerTick*self.xratio/4.0)
        elif(self.movingDirection == "LEFT"):
            xoffset = 0-round(self.innerTick*self.xratio/4.0)
        elif(self.movingDirection == "UP"):
            yoffset = 0-round(self.innerTick*self.yratio/4.0)
        elif(self.movingDirection == "DOWN"):
            yoffset = round(self.innerTick*self.yratio/4.0)
        
        self.rect.x = round(self.posx*self.xratio) + self.baseX + xoffset
        self.rect.y = round(self.posy*self.yratio) + self.baseY + yoffset
    def updateSetDirection(self, direction):
        if self.mode == 1:
            #print("Updating direction to: ",direction)
            #print("moving direction is: ", self.movingDirection)
            self.setDirection = direction
    def release(self):
        print("Releasing")
        self.trapped = False
    def update(self):
        if(self.mode == 1):
            if(self.moving):
                self.innerTick = (self.innerTick + 1) % 4
            if self.innerTick == 0: # special case 1
                if(self.moving):
                    if(self.movingDirection == "UP"):
                        self.posy -= 1
                    elif(self.movingDirection == "DOWN"):
                        self.posy += 1
                    elif(self.movingDirection == "LEFT"):
                        self.posx = (self.posx-1)%(self.boardMaxX+1)
                    elif(self.movingDirection == "RIGHT"):
                        self.posx = (self.posx+1)%(self.boardMaxX+1)
                if(self.movingDirection != self.setDirection):
                    if self.setDirection == "UP":
                        #print("set direction is up")
                        if(self.posy > 0):
                            #print("post is greater 0")
                            if( self.gmap[self.posy-1][self.posx] ==1): # not a wall
                                self.movingDirection = "UP"
                                #print("changing moving direction")
                            elif(self.gmap[self.posy-1][self.posx]==2 and not self.trapped):
                                self.movingDirection = "UP"
                        else:
                            pass # Do nothing
                    elif self.setDirection == "DOWN":
                        if(self.posy < len(self.gmap) -1): 
                            if(self.gmap[self.posy+1][self.posx] ==1): # not a wall
                                self.movingDirection = "DOWN"
                        else:
                            pass # Do nothing
                    elif self.setDirection == "RIGHT":
                        if(self.posx != self.boardMaxX):
                            if(self.posx < len(self.gmap[0]) -1):
                                if( self.gmap[self.posy][self.posx+1] ==1): # not a wall
                                    self.movingDirection = "RIGHT"
                                elif( self.gmap[self.posy][self.posx+1] == 3): # portal to the other side
                                    self.movingDirection = "RIGHT"
                                
                            else:
                                pass # Do nothing
                        else:
                            pass
                    elif self.setDirection == "LEFT":
                        if(self.posx != 0):
                            if(self.posx > 0):
                                if(self.gmap[self.posy][self.posx-1] ==1): # not a wall
                                    self.movingDirection = "LEFT"
                                elif( self.gmap[self.posy][self.posx-1] == 3): # portal
                                    self.movingDirection = "LEFT"
                            else:
                                pass # Do nothing
                        else:
                            pass
                    
                if self.movingDirection == "UP":
                    if( self.posy > 0):
                        if(self.gmap[self.posy-1][self.posx] ==1): # not a wall
                            self.moving = True
                        elif(self.gmap[self.posy-1][self.posx] == 2 and not self.trapped):
                            self.moving = True
                        else:
                            self.moving = False
                    else:
                        self.moving = False
                elif self.movingDirection == "DOWN":
                    if(self.posy < len(self.gmap)-1):
                        if (self.gmap[self.posy+1][self.posx] ==1 ): # not a wall
                            self.moving = True
                        else:
                            self.moving = False
                    else:
                        self.moving = False
                elif self.movingDirection == "RIGHT":
                    if(self.posx < (len(self.gmap[0]) -1)):
                        ##print(self.gmap[self.posx+1])
                        if( self.gmap[self.posy][self.posx+1] ==1 or self.gmap[self.posy][self.posx+1] == 3): # not a wall
                            self.moving = True
                            print("self.posx", self.posx)
                        else:
                            self.moving = False
                    else:
                        if(self.gmap[self.posy][self.posx] == 3):
                            self.moving = True
                        else:
                            self.moving = False
                        
                elif self.movingDirection == "LEFT":
                    if(self.posx > 0):
                        if(self.gmap[self.posy][self.posx-1] ==1 or self.gmap[self.posy][self.posx-1] == 3): # not a wall
                            self.moving = True
                        else:
                            self.moving = False
                    else:
                        if(self.gmap[self.posy][self.posx] == 3):
                            self.moving = True
                        else:
                            self.moving = False
        
            self.calcRect()
            self.image = self.ghostImages[self.movingDirection][self.innerTick]
    def setMode(self, mode):
        self.mode = mode

    

        
