import pygame
from pygame.locals import *
from spritesheet import *
import json

class pacman(pygame.sprite.Sprite):
    def __init__(self, gs, mode, gmap, board, items, ghosts):
        super(pacman, self).__init__()
        self.gs = gs
        self.mode = mode
        self.gmap = gmap
        self.board = board
        self.items = items
        self.ghosts = ghosts
        self.yratio = (self.board.rect.height - 34.0)/len(self.gmap)
        self.xratio = (self.board.rect.width -10)/len(self.gmap[0])
        self.stuck = False
        self.spritefile = "pacman.sprite"
        ss = spritesheet(self.spritefile)
        self.black = (0,0,0)
        self.dead = False
        self.powered = False # True if ate power pellet
        self.atePowerPTime = 0 # Time when the power pellet was consumed
        self.pacmanImages = dict()
        # Below we load a sprite twice to keep the order in which it moves. We sacrifice memory for easier coding
        #self.pacmanImages["RIGHT"] = ss.images_at(((20,90,14,14), (3,90,14,14),(20,90,14,14),(35,90,9,14)), colorkey=self.black)
        #self.pacmanImages["LEFT"]  = ss.images_at(((46,90,14,14), (3,90,14,14),(46,90,14,14),(60,90,12,14)), colorkey=self.black)
        #self.pacmanImages["UP"]    = ss.images_at(((75,90,14,14), (3,90,14,14),(75,90,14,14),(92,90,14,14)), colorkey=self.black)
        #self.pacmanImages["DOWN"]  = ss.images_at(((109,90,14,14),(3,90,14,14),(109,90,14,14),(126,90,14,14)),colorkey=self.black)
        
        self.pacmanImages["RIGHT"] = ss.images_at(((20,90,12,14), (3,90,14,14),(20,90,12,14),(35,90,9,14)), colorkey=self.black)
        self.pacmanImages["LEFT"]  = ss.images_at(((48,90,12,14), (3,90,14,14),(48,90,12,14),(63,90,9,14)), colorkey=self.black)
        self.pacmanImages["UP"]    = ss.images_at(((75,92,14,12), (3,90,14,14),(75,92,14,12),(92,95,14,9)), colorkey=self.black)
        self.pacmanImages["DOWN"]  = ss.images_at(((109,92,14,12),(3,90,14,14),(109,92,14,12),(126,95,14,9)),colorkey=self.black)
        
        # Load Death Images
        self.deathImages = ss.images_at(((3,111,16,8), (22,113,16,6),(41,114,16,5),(60,114,16,5),(79,113,16,6),(98,112,14,7),(115,112,10,7),(128,113,6,6),(137,113,2,6),(142,109,12,10),(142,92,14,14)), colorkey=self.black)
        
        # Scale images
        for key, imageL in self.pacmanImages.iteritems():
            for n in range(4):
                rect = imageL[n].get_rect()
                w = round(rect.width*self.board.ratio*0.8)
                h = round(rect.height*self.board.ratio*0.8)
                imageL[n] = pygame.transform.scale(imageL[n], (int(w), int(h)))
        for n in range(len(self.deathImages)):
            rect = self.deathImages[n].get_rect()
            w = round(rect.width*self.board.ratio*0.8)
            h = round(rect.height*self.board.ratio*0.8)
            self.deathImages[n] = pygame.transform.scale(self.deathImages[n], (int(w), int(h)))
        
        self.moving = True
        self.rect = [0,0,0,0]
        self.innerTick = 0
        self.deadTick = 0
        self.posx = 9
        self.posy = 19
        self.baseX = self.board.rect.x + 10
        self.baseY = self.board.rect.y + 18
        self.boardMaxY = len(self.gmap)-1
        self.boardMaxX = len(self.gmap[0])-1
        self.movingDirection = "RIGHT" # Current direction moving in
        self.setDirection = "RIGHT"    # Next direction to switch to
        self.iter = 0
        self.image = self.pacmanImages[self.movingDirection][1]
        self.toTick = True
    def calcRect(self):
        # Re-scale the sprites
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
        
        self.rect.x = round(self.posx*self.xratio) + self.baseX + xoffset + round(11 -self.rect.width/2.0)
        self.rect.y = round(self.posy*self.yratio) + self.baseY + yoffset + round(11 -self.rect.height/2.0)
        #self.rect.x = round(self.posx*self.xratio) + self.baseX + xoffset #+ round(10 -self.rect.width/2)
        #self.rect.y = round(self.posy*self.yratio) + self.baseY + yoffset #+ round(10 - self.rect.height/2)

    def updateSetDirection(self, direction):
        if self.mode == 1:
            #print("moving direction is: ", self.movingDirection)
            self.setDirection = direction

    def update(self):
        if(self.mode == 1):
            if(self.dead):
                if(self.deadTick < len(self.deathImages)):
                    #print("Pac is dead")
                    self.image = self.deathImages[int(self.deadTick)]
                    self.deadTick += 1
                else:
                    self.gs.ghostWon()
            else:     
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
                            else:
                                self.moving = False
                        else:
                            self.moving = False
                    elif self.movingDirection == "DOWN":
                        if(self.posy < len(self.gmap)-1):
                            if (self.gmap[self.posy+1][self.posx] == 1): # not a wall
                                self.moving = True
                            else:
                                self.moving = False
                        else:
                            self.moving = False
                    elif self.movingDirection == "RIGHT":
                        if(self.posx < (len(self.gmap[0]) -1)):
                            ##print(self.gmap[self.posx+1])
                            if( self.gmap[self.posy][self.posx+1] ==1 or self.gmap[self.posy][self.posx+1] == 3 ): # not a wall
                                self.moving = True
                            else:
                                self.moving = False
                        else:
                            if(self.gmap[self.posy][self.posx] == 3):
                                self.moving = True
                            else:
                                self.moving = False
                            
                    elif self.movingDirection == "LEFT":
                        if(self.posx > 0):
                            if(self.gmap[self.posy][self.posx-1] ==1 or self.gmap[self.posy][self.posx-1] == 3 ): # not a wall
                                self.moving = True
                            else:
                                self.moving = False
                        else:
                            if(self.gmap[self.posy][self.posx] == 3 ):
                                self.moving = True
                            else:
                                self.moving = False

                    if self.powered:
                        # De-power the ghost 8 seconds after eating power pellet
                        if(pygame.time.get_ticks() - self.atePowerPTime > 8000):
                            self.powered = False
                            for g in self.ghosts:
                                g.spooked = False
                        # Blink the ghost 6 seconds after eating power pellet
                        if(pygame.time.get_ticks() - self.atePowerPTime > 6000):
                            for g in self.ghosts:
                                g.blink = True


                    # Collide with item and ghosts
                    if(self.items[self.posy][self.posx].iType == "POWERP"):
                        self.powered = True
                        # Keep track of time the item was consumed
                        self.atePowerPTime = pygame.time.get_ticks()
                        # Turn all ghosts to 'spooked'
                        for g in self.ghosts:
                            g.spooked = True

                    self.items[self.posy][self.posx].collide()

                    for g in self.ghosts:
                        if(self.posx == g.posx and self.posy == g.posy and not self.powered):
                            self.dead = True
                            self.moving = False
                            #self.innerTick = 0
                        elif(self.posx == g.posx and self.posy == g.posy and self.powered):
                            g.dead = True
                            self.gs.pacmanWon()

                self.image = self.pacmanImages[self.movingDirection][self.innerTick]
            self.calcRect()
    def setMode(self, mode):
        self.mode = mode
    def checkCollision(self, posx, posy):
        for g in self.ghosts:
            if(posx == g.posx and posy == g.posy):
                self.dead = True
                self.moving = False
                #self.innerTick = 0
                return True
        return False
         
    

        
