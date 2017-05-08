import pygame
from pygame.locals import *
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from pacman import pacman
from board import board
from ghost import ghost
from items import items
# Array used to move around map
# 0 equals wall
# 1 equals path
# 2 equals gate
# 3 equals portal
gmap=[ [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1]
      ,[1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1]
      ,[1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1]
      ,[0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,1,0,2,2,2,0,1,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,0,0]
      ,[3,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,3]
      ,[0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0]
      ,[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1]
      ,[0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0]
      ,[0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0]
      ,[1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1]
      ,[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1]
      ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

# 0 = empty
# 1 = regular Dot
# 2 = Special Dot
# 3 = light
imap=[ [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[2,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,2]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1]
      ,[1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1]
      ,[1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1]
      ,[2,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,2]
      ,[0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0]
      ,[0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0]
      ,[1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1]
      ,[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1]
      ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
tmap=[ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0]
      ,[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ,[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
#imap = tmap
class GameSpace():
    def redraw(self):
        self.screen.blit(self.background, (0,0))
        self.allsprites.draw(self.screen)
        pygame.display.flip()

    def __init__(self):
        pygame.init()
        self.height = 640
        self.width = 640
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        self.mode = 1 # start in pause
        pygame.mouse.set_visible(0)
        
        # Create Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0,0,0))

        # Create Clock
        self.clock = pygame.time.Clock()
        self.going = False
        # Create Objects
        self.allsprites = pygame.sprite.OrderedUpdates()
        self.board = board(self)
        self.items = items(self, self.mode, imap, self.board)
        self.ghosts = list()
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "RED"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "CYAN"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "ORANGE"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "PINK"))
        self.pacman = pacman(self, self.mode, gmap, self.board,self.items.getItemsList(),self.ghosts)
        self.player = self.pacman
        self.allsprites.add(self.ghosts)
        self.allsprites.add(self.pacman)
        self.allsprites.add(self.board)
        for i in self.items.getItemsList():
            self.allsprites.add(i)
        #self.ghosts = list()
        for n in range(4):
            #self.ghosts.append(ghost.ghost(self.mode))
            #self.allsprites.add(self.ghosts[n])
            pass

        # Allow user to press down on key
        #pygame.key.set_repeat(500,30)

    def main(self):
        self.going = True
        distance = 5
        while self.going:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.player.updateSetDirection("UP")
                    elif event.key == K_DOWN:
                        self.player.updateSetDirection("DOWN")
                    elif event.key == K_RIGHT:
                        self.player.updateSetDirection("RIGHT")
                    elif event.key == K_LEFT:
                        self.player.updateSetDirection("LEFT")
                    elif event.key == K_q:
                        self.going = False
                    elif event.key == K_r:
                        self.ghost.release()
                elif event.type == QUIT:
                    self.going = False
            self.allsprites.update() # tick
            self.redraw()
        
        pygame.quit()
    def pacmanWon(self):
        print("Pacman won!!!")
        self.going = False
    def ghostWon(self):
        print("Ghost won!!!")
        self.going = False
if __name__ == "__main__":
    gs = GameSpace()
    gs.main()
