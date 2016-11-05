
'''
{
u'hardBlockBoard': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
u'boardSize': 11, 
u'gameID': u'581a7198eeaffac310f17655', 
u'bombMap': {}, 
u'moveIterator': 0, 
u'playerID': u'581a7198eeaffac310f17653', 
u'portalMap': {
  u'3,1': {}
}, 
u'playerIndex': 0, 
u'trailMap': {
  u'0,1': {
    u'0': {
      u'tick': 1, 
      u'type': u'h'
    }
  }, 
  u'1,2': {
    u'0': {
      u'tick': 1, 
      u'type': u'v'
    }
  }, 
  u'3,1': {
    u'0': {
      u'tick': 1, 
      u'type': u'h'
    }
  }, 
  u'1,0': {u'0': {u'tick': 1, u'type': u'v'}}, 
  u'1,1': {u'0': {u'tick': 1, u'type': u'origin'}}, 
  u'2,1': {u'0': {u'tick': 1, u'type': u'h'}}, 
  u'1,3': {u'0': {u'tick': 1, u'type': u'v'}}}, 
u'player': {
  u'bluePortal': None, 
  u'orientation': 3, 
  u'orangePortal': None, 
  u'coins': 20, 
  u'bombCount': 1, 
  u'bombPierce': 0, 
  u'alive': False, 
  u'y': -1, 
  u'x': -1, 
  u'bombRange': 3
}, 
u'state': u'complete', 
u'softBlockBoard': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
u'moveOrder': [1, 0], 
u'opponent': {
  u'bluePortal': None, 
  u'orientation': 3, 
  u'orangePortal': None, 
  u'coins': 0, 
  u'bombCount': 1, 
  u'bombPierce': 0, 
  u'alive': True, 
  u'y': 9, 
  u'x': 9, 
  u'bombRange': 3
}
}
'''

import random as r

def tryish(error, f, *args, **kargs):
    try:
        return f(*args, **kargs)
    except error:
        pass
    return None

def gridToListIndex(rowLen, x, y):
    return x * rowLen + y

def listToGridPos(rowLen, i):
    return (i / rowLen, i % rowLen)

oppMap = {'u':'d', 'd':'u', 'l':'r', 'r':'l', 'h':'h'}
dirMap = {'u':1, 'd':3, 'l':0, 'r':2, 'h':-1, -1:'h', 2:'r', 0:'l', 3:'d', 1:'u'}

class Dir:
    def __init__(self, dir):
        try:
            self.dir = dirMap[int(dir)]
        except ValueError:
            self.dir = dir

    def __str__(self):
        return self.dir

    def __hash__(self):
        return hash(self.dir)

    def __int__(self):
        return dirMap[self.dir]

    def __eq__(self, other):
        try:
            return self.dir == other.dir
        except AttributeError:
            pass
        
        return self.dir == other or self.dir == dirMap[other]

    def opposite(self):
        return Dir(oppMap[self.dir])



class Pos:
    def __init__(self, x, y = None):
        if y is None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return '%s,%s' % (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            pass
        
        return self.x == other[0] and self.y == other[1]

    def getAdj(self):
        l = {}
        l['u'] = Pos(self.x, self.y - 1)
        l['d'] = Pos(self.x, self.y + 1)
        l['l'] = Pos(self.x - 1, self.y)
        l['r'] = Pos(self.x + 1, self.y)
        return l

    def getDir(self, dir):
        if dir == 'u':
            return Pos(self.x, self.y - 1)
        elif dir == 'd':
            return Pos(self.x, self.y + 1)
        elif dir == 'l':
            return Pos(self.x - 1, self.y)
        elif dir == 'r':
            return Pos(self.x + 1, self.y)
        elif dir == 'h':
            return self
        return None

class Portal:
    def __init__(self, pos, color, direction, owner, other = None):
        self.pos = pos
        self.color = color
        self.direction = direction
        self.owner = owner
        self.addOther(other)

    def addOther(self, other):
        self.other = other
        if self.color == 'orange':
            self.orange = self
            self.blue = other
        else:
            self.orange = other
            self.blue = self

class Tile:
    def __init__(self, pos, hasHard, hasSoft, trailMaxCount, bombCount, portals):
        self.pos = pos
        self.hard = bool(hasHard)
        self.soft = bool(hasSoft)
        self.trail = tryish(TypeError, int, trailMaxCount)
        self.bomb = tryish(TypeError, int, bombCount)
        self.portals = portals

    def __str__(self):
        return 'pos = %s, hard = %s, soft = %s, trail = %s, bomb = %s, portals = %s' %(self.pos, self.hard, self.soft, self.trail, self.bomb, self.portals)

        #      P|#

    # 
    def walkable(self, dir):
        '''
          is walkable from dir
          P|#
          True if dir == 'r'
        '''
        if self.bomb or self.trail:
            return False

        if self.portals is None:
            if self.hard or self.soft:
                return False
            return True

        for p in self.portals:
            if p.direction == dir.opposite() and p.other is not None:
                return True

        return False

class Board:
    def __init__(self, game, size, hardBlockBoard, softBlockBoard, trailMap, bombMap, portalMap):
        self.game = game
        self.board = {}
        self.bombs = {}
        self.bombCount = {0:0, 1:0}
        self.trails = set([])

        for n, (h, s) in enumerate(zip(hardBlockBoard, softBlockBoard)):
            pos = Pos(listToGridPos(size, n))
            posStr = str(pos)

            def getTrail():
                trail = trailMap[posStr]
                p = tryish(KeyError, trail.__getitem__, '0'), tryish(KeyError, trail.__getitem__, '1')
                self.trails.add(pos)
                if p[0] is None and p[1] is None:
                    return None
                if p[0] is None:
                    return int(p[1]['tick'])
                if p[1] is None:
                    return int(p[0]['tick'])
                return max(*[i['tick'] for i in p])

            def getBomb():
                bomb = bombMap[posStr]
                self.bombs[pos] = bomb['owner']
                self.bombCount[bomb['owner']] += 1
                return bomb['tick']

            def getPortal():
                allPortals = {}
                portal = portalMap[posStr]
                for d in portal:
                    thisPortal = portal[d]
                    d = Dir(d)
                    allPortals[d] = Portal(pos, thisPortal['portalColor'], d, thisPortal['owner'])
                return allPortals

            t = tryish(KeyError, getTrail)
            b = tryish(KeyError, getBomb)
            p = tryish(KeyError, getPortal)
            #                  pos, hasHard, hasSoft, trailMaxCount, bombCount, portals
            self.board[pos] = Tile(pos, h, s, t, b, p)
                
        self.size = (size, size)

    def __str__(self):
        s = ''
        for p in self.board:
            s += str(self.board[p]) + '\n'
        return s

    def __getitem__(self, pos):
        try:
            return self.board[pos]
        except KeyError:
            pass

        return None

    def isNextToSoft(self, pos):
        for d, p in pos.getAdj().iteritems():
            tile = self[p]
            if tile is not None and tile.soft:
                return d
        return None

    def isNextToBomb(self, pos):
        if self[pos].bomb:
            return 'h'
        for d, p in pos.getAdj().iteritems():
            if self.board[p].bomb:
                return d
        return None

    def distToBomb(self, pos):
        d = sum(self.size) + 100
        for p in self.bombs:
            playerNum = self.bombs[p]
            bombDist = self.game.getPlayer(playerNum).bombRange
            if p.x == pos.x:
                dist = abs(p.x - pos.x)
                if dist <= bombDist and dist < d:
                    d = dist

            if p.y == pos.y:
                dist = abs(p.y - pos.y)
                if dist <= bombDist and dist < d:
                    d = dist

        return d

class Player:
    def __init__(self, data, board, index):
        self.orientation = data['orientation']
        self.coins = data['coins']
        self.pos = Pos(data['x'], data['y'])
        self.bombCount = data['bombCount']
        self.bombPierce = data['bombPierce']
        self.bombRange = data['bombRange']
        self.alive = data['alive']
        self.board = board
        self.index = index
        self.bombsInPlay = board.bombCount[self.index]

        self.orange = None
        o = data['orangePortal']
        if o is not None:
            opos = Pos(o['x'], o['y'])
            odir = Dir(o['direction'])
            # TODO: fix self.board[opos].portals should never be None
            if self.board[opos].portals is not None:
                self.orange = self.board[opos].portals[odir]

        self.blue = None
        b = data['bluePortal']
        if b is not None:
            bpos = Pos(b['x'], b['y'])
            bdir = Dir(b['direction'])
            if self.board[bpos].portals is not None:
                self.blue = self.board[bpos].portals[bdir]

        if self.orange is not None:
            self.orange.addOther(self.blue)
        if self.blue is not None:
            self.blue.addOther(self.orange)

    def canPlaceBomb(self):
        return self.bombCount - self.bombsInPlay > 0
    
    def bestBuy(self):
        if self.coins < 1:
            return None

        if self.bombPierce < self.bombRange:
            return 'buy_pierce'
        elif self.bombRange < 10:
            return 'buy_range'
        elif self.bombCount < 5:
            return 'buy_count'

    def isNextToSoft(self):
        return self.board.isNextToSoft(self.pos)

    def isNextToBomb(self):
        return self.board.isNextToBomb(self.pos)

    def distToBomb(self):
        return self.board.distToBomb(self.pos)

    def walkable(self):
        dirs = {}
        for d, p in self.pos.getAdj().iteritems():
            t = self.board[p]
            if t.walkable(d):
                dirs[d] = self.board.distToBomb(p)
        return dirs

    def bestWalk(self):
        ret = ((None,), -100)
        for d, p in self.pos.getAdj().iteritems():
            t = self.board[p]
            if t is not None and t.walkable(d):
                qual = self.board.distToBomb(p)
                print 'd = %s, p = %s, qual = %s' % (d, p, qual)
                if qual > ret[1]:
                    ret = ((d,), qual)
                elif qual == ret[1]:
                    ret = (ret[0] + (d,), qual)
        if len(ret[0]) == 1:
            return (ret[0][0], ret[1])
        else:
            return (r.choice(ret[0]), ret[1])

class BommerGame:
    def __init__(self, data):
        self.init(data)

    def init(self, data):
        self.state = None
        try:
            self.board =        Board(game = self,
                                size = data[u'boardSize'], 
                                hardBlockBoard = data[u'hardBlockBoard'], 
                                softBlockBoard = data[u'softBlockBoard'],
                                trailMap = data[u'trailMap'], 
                                bombMap = data[u'bombMap'],
                                portalMap = data[u'portalMap'])
            self.moveOrder =    data[u'moveOrder']
            self.playerIndex =  data[u'playerIndex']
            self.moveIterator = data[u'moveIterator']

            self.player =       Player(data[u'player'], self.board, self.playerIndex)
            self.opponent =     Player(data[u'opponent'], self.board, 1 - self.playerIndex)

            self.gameID =       data[u'gameID']
            self.playerID =     data[u'playerID']

            self.state =        data[u'state']
        except TypeError:
            pass

    def __bool__(self):
        '''
        Returns true iff the game is in progress
        '''
        return self.state == 'in progress'

    def getPlayer(self, index):
        if index == self.playerIndex:
            return self.player
        return self.opponent

    def ended(self):
        return self.state == 'complete'

    def update(self, data):
        self.init(data)

    def move(self):
        #availableDirs = self.player.walkable()
        act = ''
        b = self.player.distToBomb()
        d, qual = self.player.bestWalk()
        buy = self.player.bestBuy()

        if d is not None:
            act = 'm' + str(d)

        print 'dist = %s, soft = %s, can bomb = %s' % (b, self.player.isNextToSoft() is not None, self.player.canPlaceBomb())

        # If near bomb, move away
        if b <= sum(self.board.size):
            if d is not None:
                print 'If near bomb, move away'
                act = 'm' + str(d)
                
        # If near soft and can place bomb, do so
        elif self.player.isNextToSoft() is not None and self.player.canPlaceBomb():
            print 'If near soft and can place bomb, do so'
            act = 'b'

        # If safe and have $$, buy stuff
        elif buy is not None:
            print 'If safe and have $%s, buy stuff' % self.player.coins
            act = buy

        print 'act = %r' % act
        return act

        

            
