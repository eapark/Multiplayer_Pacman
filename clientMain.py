import pygame
from pygame.locals import *
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
import threading
import json
from preScreen import preScreen
from finalScreen import finalScreen
import Queue
import sys
from pacman import pacman
from board import board
from ghost import ghost
from items import items
import collections
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
    
    def __init__(self, gf):
        self.connected = False
        pygame.init()
        self.factory = gf
        self.closed = False
        self.factory.setGS(self)
        self.winner = None
        self.height = 640
        self.width = 640
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        self.mode = 1 # start in pause
        self.index = -1 # used to identify which ghost the player is
        self.numPlayers = 0 # counts other players
        pygame.mouse.set_visible(0)
        self.addedFactory = False
        
        # Create Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0,0,0))

        # Create Clock
        self.clock = pygame.time.Clock()
        self.going = False
        # Create Objects
        self.allsprites = pygame.sprite.OrderedUpdates()
        self.board = board(self)
        self.preScreen = preScreen(self, "Connecting to Server...")
        self.items = items(self, self.mode, imap, self.board)
        self.ghosts = list()
        self.sendingEvents = list()
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "RED"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "CYAN"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "ORANGE"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "PINK"))
        self.pacman = pacman(self, self.mode, gmap, self.board,self.items.getItemsList(),self.ghosts)
        self.player = None
        for i in self.items.getItemsList():
            self.allsprites.add(i)
        self.allsprites.add(self.ghosts)
        self.allsprites.add(self.pacman)
        self.allsprites.add(self.board)
       
        # Allow user to press down on key
        #pygame.key.set_repeat(500,30)

    def main(self):
        self.going = True
        self.connected = False
        distance = 5

        while(not self.connected):
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        self.connected = True
                        self.going = False
                        self.closed = True
                elif event.type == QUIT:
                    self.connected = True
                    self.going = False
                    self.closed = True
            
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.preScreen.image, self.preScreen.rect)
            pygame.display.flip()
        # Process Received Data
        if(self.going):
            pdata = self.factory.connection.getData()
            data = json.loads(pdata)
            while(data['request'] != 'start'):
                if(data['request'] == 'init'):
                    self.index = data['index']
                    self.player = self.ghosts[self.index]
                elif(data['request'] == 'updatePlayers'):
                    self.numPlayers = data['numConns']
                pdata = self.factory.connection.getData()
                #print("pdata is ", pdata)
                #print(" <<<<<<<<<")
                data = json.loads(pdata)
            #print("self.index: ", self.index)
            #print("self.numPlayers: ", self.numPlayers)

        while self.going:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.sendingEvents.append("UP")
                        self.player.updateSetDirection("UP")
                    elif event.key == K_DOWN:
                        self.sendingEvents.append("DOWN")
                        self.player.updateSetDirection("DOWN")
                    elif event.key == K_RIGHT:
                        self.sendingEvents.append("RIGHT")
                        self.player.updateSetDirection("RIGHT")
                    elif event.key == K_LEFT:
                        self.sendingEvents.append("LEFT")
                        self.player.updateSetDirection("LEFT")
                    elif event.key == K_q:
                        self.going = False
                        self.closed = True
                elif event.type == QUIT:
                    self.going = False
                    self.closed = True
            self.sendEvents()
            self.processForeignEvents()

            self.allsprites.update() # tick
            self.redraw()

        self.final = finalScreen(self, "{} Won!!!".format(self.winner))
        tobreak = False
        if(not self.closed):
            for i in range(30):
                self.clock.tick(30)
                self.screen.blit(self.background, (0,0))
                self.screen.blit(self.final.image, self.final.rect)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        tobreak = True
                if(tobreak):
                    break
        pygame.quit()
        reactor.callFromThread(reactor.stop)
    def sendEvents(self):
        # Send imap, position of pacman and ghosts, whether ghost is spooked or not
        data = dict()
        data["request"] = "update"
        data['type'] = 'ghost'
        data['index'] = self.index
        data['events'] = self.sendingEvents

        self.factory.connection.sendData(json.dumps(data))
        del self.sendingEvents[:]
        
    def processForeignEvents(self):
        #print("Processing foreign Events")
        numUpdates = 0
        while(numUpdates < self.numPlayers):
            try:
                pdata = self.factory.connection.getData() # Blocking call until data is received
                data = json.loads(pdata)
                #print("In processing events data is ", data)
                if(data['request'] == 'update'):
                    if(data['type'] == 'pacman'):
                        player = self.pacman
                    else:
                        player = self.ghost[data['index']]
                    events = data['events']
                    #print("In processing events events is ", events)
                    for event in events:
                            #print("Player is", player)
                            if(event == "UP"):
                                player.updateSetDirection("UP")
                            elif(event == "DOWN"):
                                player.updateSetDirection("DOWN")
                            elif(event == "RIGHT"):
                                player.updateSetDirection("RIGHT")
                            elif(event == "LEFT"):
                                player.updateSetDirection("LEFT")
                    numUpdates += 1
                elif(data['request'] == 'release'):
                    self.player.release()
                else:
                    print("Unhandled message", data)
            except ValueError as e:
                print("pdata: ", pdata)
                print("The following Error has Occurred: ", e)
                print("Quitting...")
                sys.exit(1)

    def pacmanWon(self):
        #print("Pacman won!!!")
        self.going = False
        self.winner = "pacman"
    def ghostWon(self):
        #print("Ghost won!!!")
        self.going = False
        self.winner = "ghost"

class GameConnection(Protocol, object):
    def __init__(self, Factory):
        super(GameConnection, self).__init__()   # 
        self.factory = Factory
        self.gs = None
        #self.lock = Threading.Lock()
        self.condVar = threading.Condition()
        self.queue = collections.deque()
        self.qcount = 0
    def connectionMade(self):
        self.gs.connected = True
    def dataReceived(self, data):
        #print("Received data", data)
        self.condVar.acquire()
        self.queue.append(data)
        self.qcount += 1
        self.condVar.notify()
        self.condVar.release()
    def getData(self):
        data = None
        self.condVar.acquire()
        while self.qcount == 0:
            self.condVar.wait()
        pdata = self.queue.popleft()
        sdata = pdata.split('{')
        del sdata[0] # should be empty
        for n in range(len(sdata)):
            sdata[n] = '{' + sdata[n]
        if(len(sdata) > 1):
            for s in sdata[1:]:
                self.qcount += 1
                self.queue.appendleft(s)
        data = sdata[0]

        self.qcount -= 1
        self.condVar.release()

        return data
        
    def connectionLost(self, reason):
        pass
        #print("Connection lost with server. Quitting...")
        #print("Reason: ", reason)
        #sys.exit(1)

    def sendData(self, data):
        self.transport.write(data)
    def setGS(self, gs):
        self.gs = gs

class GameFactory(ClientFactory, object):
    def __init__(self):
        self.connection = GameConnection(self)
    def buildProtocol(self, addr):
        return self.connection
    def setGS(self, gs):
        self.gs = gs
        self.connection.setGS(self.gs)

class runGame(threading.Thread):
    def __init__(self, gf):
        threading.Thread.__init__(self)
        self.gs = GameSpace(gf)
    def run(self):
        #print("Running GS")
        self.gs.main()


if __name__ == "__main__":
    gf = GameFactory()
    rn = runGame(gf)
    rn.daemon = True
    rn.start()
    reactor.connectTCP("ash.campus.nd.edu",40049, gf)
    reactor.run()

