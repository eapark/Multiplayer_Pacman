import pygame
from pygame.locals import *
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
import threading
#import cPickle
import json
import Queue
import sys
from pacman import pacman
from board import board
from ghost import ghost
from items import items
from preScreen import preScreen
from finalScreen import finalScreen
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
        pygame.init()
        self.factory = gf
        self.factory.setGS = self
        self.winner = "NONE"
        self.height = 640
        self.width = 640
        self.releaseIndex = 0
        self.closed = False
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        self.mode = 1 # start in pause
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
        self.preScreen = preScreen(self, "Waiting for Connections. Press Space to Continue")
        self.items = items(self, self.mode, imap, self.board)
        self.ghosts = list()
        self.sendingEvents = list()
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "RED"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "CYAN"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "ORANGE"))
        self.ghosts.append(ghost(self, self.mode, gmap, self.board, "PINK"))
        self.pacman = pacman(self, self.mode, gmap, self.board,self.items.getItemsList(),self.ghosts)
        self.player = self.pacman
        for i in self.items.getItemsList():
            self.allsprites.add(i)
        self.allsprites.add(self.ghosts)
        self.allsprites.add(self.pacman)
        self.allsprites.add(self.board)

        # Allow user to press down on key
        #pygame.key.set_repeat(500,30)

    def main(self):
        self.going = True
        self.waitingConnection = True
        distance = 5

        while(self.waitingConnection):
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.waitingConnection = False
                        self.closed = True
                if event.type == QUIT:
                    self.waitingConnection = False
                    self.going = False
                    self.closed = True
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.preScreen.image, self.preScreen.rect)
            pygame.display.flip()
        
        
        # Send numConn

        for conn in self.factory.conns:
            #if(conn.index != self.index):
            data = dict()
            data['request'] = 'updatePlayers'
            data['numConns'] = self.factory.numConns
            conn.sendData(json.dumps(data))
        # Send start
        for conn in self.factory.conns:
            data = dict()
            data['request'] = 'start'
            conn.sendData(json.dumps(data))
            
        pygame.time.set_timer(USEREVENT + 1, 5000)
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
                    elif event.key == K_r:
                        self.ghost.release()
                elif event.type == QUIT:
                    self.going = False
                    self.closed = True
                elif event.type == USEREVENT + 1:
                    self.releaseGhost()
            self.sendEvents()
            self.processForeignEvents()

            self.allsprites.update() # tick
            self.redraw()
        
        self.final = finalScreen(self, "{} won!!!".format(self.winner))
        tobreak = False
        if not self.closed:
            for i in range(30):
                self.clock.tick(30)
                self.screen.blit(self.background, (0,0))
                self.screen.blit(self.final.image, self.final.rect)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        tobreak = True
                        break
                if tobreak:
                    break

        pygame.quit()
        reactor.callFromThread(reactor.stop)
    def sendEvents(self):
        # Send imap, position of pacman and ghosts, whether ghost is spooked or not
        data = dict()
        data["request"] = "update"
        data['type'] = 'pacman'
        data['events'] = self.sendingEvents
        
        for n in range(self.factory.numConns):
            self.factory.conns[n].sendData(json.dumps(data))

        del self.sendingEvents[:]
    def releaseGhost(self):
        self.ghosts[self.releaseIndex].release()
        if(self.releaseIndex < self.factory.numConns):
            data = dict()
            data['request'] = "release"
            self.factory.conns[self.releaseIndex].sendData(json.dumps(data))
        self.releasedIndex = (self.releaseIndex + 1) % 4
    def processForeignEvents(self):
        for n in range(self.factory.numConns):
            try:
                pdata = self.factory.conns[n].getData() # Blocking call until data is received
                data = json.loads(pdata)
                if(data['request'] == 'update'):
                    events = data['events'] 
                    for event in events:
                        if event == "UP":
                            self.ghosts[n].updateSetDirection("UP")
                        elif event == "DOWN":
                            self.ghosts[n].updateSetDirection("DOWN")
                        elif event == "RIGHT":
                            self.ghosts[n].updateSetDirection("RIGHT")
                        elif event == "LEFT":
                            self.ghosts[n].updateSetDirection("LEFT")
                for m in range(self.factory.numConns):
                    if(m != n):
                        data['request'] = 'update'
                        data['type'] = 'ghost'
                        data['index'] = m
                        data['events'] = self.sendingEvents
                        self.ghosts[m].sendData(json.dumps(data))
            except Exception as e:
                print("The following Error has Occurred: ", e)
                print("Quitting...")
                reactor.callFromThread(reactor.stop)
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
    def __init__(self, Factory,index):
        super(GameConnection, self).__init__()   # 
        self.factory = Factory
        #self.gs = gs
        self.index = index
        #self.lock = Threading.Lock()
        self.condVar = threading.Condition()
        self.queue = collections.deque()
        self.dqueue = collections.deque()
        self.qcount = 0
    def dataReceived(self, data):
        self.condVar.acquire()
        self.queue.append(data)
        self.qcount+=1
        self.condVar.notify()
        self.condVar.release()
    def getData(self):
        data = None
        self.condVar.acquire()
        while self.qcount == 0:
            self.condVar.wait()
        pdata = self.queue.popleft()
        sdata = pdata.split("{")
        for n in range(len(sdata)):
            sdata[n]="{"+sdata[n]
        del sdata[0] # Should be empty str
        if(len(sdata) > 1):
            for s in sdata[1:]:
                self.queue.appendleft(s)
                self.qcount+=1
        data = sdata[0]

        self.qcount-=1
        self.condVar.release()

        return data
    def connectionMade(self):
        #print("#####Connection Made")
        data = dict()
        data['request'] = 'init'
        data['index'] = self.index
        #self.dqueue.put(json.dumps(data))
        #self.dqueue.get().addCallback(self.transport.write)
        self.transport.write(json.dumps(data))


    def connectionLost(self, reason):
        self.factory.numConns -= 1
    def sendData(self, data):
        self.transport.write(data)
    def setGS(self, gs):
        self.gs

class GameFactory(Factory):
    def __init__(self):
        self.conns = list()
        self.numConns = 0
        #print("Running Factory")
    def buildProtocol(self, addr):
        conn = GameConnection(self, self.numConns)
        self.conns.append(conn)
        self.numConns += 1
        return conn
    def getConns(self):
        return self.conns
    def setGS(self, gs):
        self.gs = gs
        for conn in self.conns:
            conn.setGS(self.gs)


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
    rn.start()
    reactor.listenTCP(40049, gf)
    reactor.run()
