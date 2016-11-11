
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

def weightedChoice(choices):
   total = sum(w for c, w in choices if w > 0)
   rand = r.uniform(0, total)
   upto = 0
   for c, w in choices:
      if w > 0:
         upto += w
         if upto >= rand:
            return c
   return r.choice(choices)[0]

def bestChoice(choices):
   best = ((None,), -100000)
   for c, w in choices:
      if w > best[1]:
         best = ((c,), w)
      elif w == best[1]:
         best = (best[0] + (c,), w)
   if len(best[0]) == 1:
      return best[0][0]
   return r.choice(best[0])

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

#possibleMoves = ['mu', 'ml', 'mr', 'md', 'tu', 'tl', 'tr', 'td', 
#                 'b', '', 'op', 'bp', 'buy_count', 'buy_range', 
#                 'buy_pierce', 'buy_block']
#possibleMoves = ['mu', 'ml', 'mr', 'md', 'b']
possibleMoves = ['mu', 'ml', 'mr', 'md',  'b', 'buy_count', 'buy_range', 'buy_pierce']

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
   
   def __getitem__(self, i):
      if i == 0:
         return self.x
      elif i == 1:
         return self.y
      raise IndexError

   def __eq__(self, other):
      try:
         return self.x == other.x and self.y == other.y
      except AttributeError:
         pass

      return self.x == other[0] and self.y == other[1]

   def getAdj(self):
      l = {}
      l[Dir('u')] = Pos(self.x, self.y - 1)
      l[Dir('d')] = Pos(self.x, self.y + 1)
      l[Dir('l')] = Pos(self.x - 1, self.y)
      l[Dir('r')] = Pos(self.x + 1, self.y)
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
   
   def dist(self, other):
      o = Pos(other)
      return abs(self.x - o.x) + abs(self.y - o.y)

class Portal:
   def __init__(self, pos, color, direction, owner, other = None):
      self.pos = pos
      self.color = color
      self.direction = direction
      self.owner = owner
      self.addOther(other)

   def __hash__(self):
      return hash((self.pos, self.color, self.direction, self.owner))

   def addOther(self, other):
      self.other = other
      if self.color == 'orange':
         self.orange = self
         self.blue = other
      else:
         self.orange = other
         self.blue = self

   def dist(self, other):
      return abs(self.pos.x - other.x) + abs(self.pos.y - other.y)

class Tile:
   def __init__(self, pos, hasHard, hasSoft, trailMaxCount, bombCount, portals):
      self.pos = pos
      self.hard = bool(hasHard)
      self.soft = bool(hasSoft)
      self.trail = tryish(TypeError, int, trailMaxCount)
      self.bomb = tryish(TypeError, int, bombCount)
      self.portals = portals

      # dict from Dir to tiles
      self.adj = {}
      self.tile = None

   def __hash__(self):
      ''' l = []
      if self.portals is not None:
         for d in self.portals:
            l.append((hash(d), hash(self.portals[d])))
         l.sort()      
      return hash((self.pos, self.hard, self.soft, self.trail, self.bomb, tuple(l)))'''
      return hash((self.pos, self.hard, self.soft, self.trail, self.bomb))

   def __str__(self):
      return 'pos = %s, hard = %s, soft = %s, trail = %s, bomb = %s, portals = %s' \
             % (self.pos, self.hard, self.soft, self.trail, self.bomb, self.portals)

      #      P|#

   # 
   def walkable(self, dir = None, dist = 0):
      '''
        is walkable from dir
        P|#
        True if dir == 'r'
      '''
      result = set([])

      if dist == 0:
         if self.bomb or self.trail:
            return result

         if self.portals is None:
            if self.hard or self.soft:
               return result
            result.add(self)
            return result

         if dir is not None:
            for p in self.portals:
               if p.direction == dir.opposite() and p.other is not None:
                  result.add(self)
                  return result

         return result

      if not self.walkable(dir):
         return result

      for d in self.adj:
         adjTile = self.adj[d]
         result.union(adjTile.walkable(d, dist - 1))

      return result


   def walk(self, dir):
      try:
         adjTile = self.adj[dir]
         if adjTile.walkable(dir):
            for p in self.portals:
               if p.direction == dir.opposite() and p.other is not None:
                  otherTile = p.other
                  otherDir = p.other.direction
                  return otherTile.walk(otherDir)
            return adjTile
      except KeyError:
         pass

      return None

class Board:
   def __init__(self, game, size, hardBlockBoard, softBlockBoard, trailMap, bombMap, portalMap):
      self.game = game
      self.board = {}
      self.bombs = {}
      self.bombCount = {0:0, 1:0}
      self.trails = set([])
      self.cache = {}
      self.myPos = None

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
      self.MAXDIST = 3 * max(self.size)

      for pos in self.board:
         tile = self.board[pos]
         for d, p in pos.getAdj().iteritems():
            try:
               adjTile = self.board[p]
               tile.adj[d] = adjTile
            except KeyError:
               pass

   def __hash__(self):
      l = []
      for pos in self.board:
         if (self.myPos is not None and self.myPos.dist(pos) <= 4) or self.myPos is not None:
            l.append((hash(pos), hash(self.board[pos])))
      l.sort()
      return hash(tuple(l))

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
      try:
         if pos in self.cache['isNextToSoft']:
            return self.cache['isNextToSoft'][pos]
      except KeyError:
         self.cache['isNextToSoft'] = {}

      for d, p in pos.getAdj().iteritems():
         tile = self[p]
         if tile is not None and tile.soft:
            self.cache['isNextToSoft'][pos] = d
            return d

      self.cache['isNextToSoft'][pos] = None
      return None

   def isNextToBomb(self, pos):
      try:
         if pos in self.cache['isNextToBomb']:
            return self.cache['isNextToBomb'][pos]
      except KeyError:
         self.cache['isNextToBomb'] = {}

      if self[pos].bomb:
         return 'h'
      for d, p in pos.getAdj().iteritems():
         if self.board[p].bomb:
            self.cache['isNextToBomb'][pos] = d
            return d

      self.cache['isNextToBomb'][pos] = None
      return None

   def distToBomb(self, pos):
      try:
         if pos in self.cache['distToBomb']:
            return self.cache['distToBomb'][pos]
      except KeyError:
         self.cache['distToBomb'] = {}

      d = self.MAXDIST + 1
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

      self.cache['distToBomb'][pos] = d
      return d

   def distToSafe(self, pos):
      tile = self.board[pos]
      if not tile.walkable():
         return self.MAXDIST + 1

      if self.distToBomb(pos) > 100:
         # No Bombs in sight
         return 0

      minDist = self.MAXDIST + 1
      for d, p in pos.getAdj().iteritems():
         for t in tile.walkable(d, 1):
            t.distToSafe(t.pos)


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
      elif self.bombRange < 15:
         return 'buy_range'
      elif self.bombCount < 5:
         return 'buy_count'

   def __hash__(self):
      return hash((self.pos, self.bombCount, self.bombPierce, self.bombRange, self.alive))
      #return hash((self.orientation, self.coins, self.pos, self.bombCount, self.bombPierce, self.bombRange, self.alive, self.index))

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
            #print 'd = %s, p = %s, qual = %s' % (d, p, qual)
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

   def __hash__(self):
      return hash((self.board, self.player, self.opponent))

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
         
         self.board.myPos = self.player.pos

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

      #print 'dist = %s, soft = %s, can bomb = %s' % (b, self.player.isNextToSoft() is not None, self.player.canPlaceBomb())

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

   def qlearn(self, filename):
      curState = hash(self)
      try:
         reward = 0
         if not self.player.alive:
            reward += -1000

         if not self.opponent.alive:
            reward += 1000
            
            
         b = self.player.distToBomb()
         if b <= sum(self.board.size):
            reward += (b - 34/2) * 10
            
         if self.lastState == curState:
            reward -= 50
            
         d, qual = self.player.bestWalk()
         if d is not None:
            reward += (qual - 34/2) * 5
            
         reward += self.player.coins

         actionSet = set([])
         for action in possibleMoves:
            try:
               qval = float(self.qvalues[(curState, action)])
               actionSet.add((action, (qval + 900) + (r.random() - .5)*250))
            except (KeyError, ValueError):
               actionSet.add((action, r.random()*1000 + 500))

         curAction = weightedChoice(actionSet)

         #try:
         #   lastVal = int(self.qvalues[(self.lastState, self.lastAction)])
         #except ValueError:
         #   lastVal = 0
            
         try:
            curVal = float(self.qvalues[(curState, curAction)])
         except ValueError:
            curVal = 0      
            
         self.lastVal = self.lastVal + self.alpha * (reward + self.gamma*curVal - self.lastVal)
         
         if self.lastVal != 0:
            self.qvalues[(self.lastState, self.lastAction)] = '%.08e' % self.lastVal

         try:
            print '%s\t% 16.08f\t%s' % (self.lastAction.ljust(10), self.lastVal, reward)
         except (TypeError, AttributeError):
            pass
         self.lastState = curState
         self.lastAction = curAction
         self.lastVal = curVal

         
         return curAction

      except AttributeError:
         # Learning rate
         self.alpha = 0.9
         # Discount factor 
         self.gamma = 0.5
         self.qvalues = hashDict(filename, 2**16, 2**4)
         self.lastState = None
         self.lastAction = None
         self.lastVal = 0

      return ''


class hashDict:
   def __init__(self, fileName, size = 2**16, width = 2**4):
      self.fileName = fileName
      try:
         with open(self.fileName, 'rb') as f:
            self.size = f.readline()
         self.width = len(self.size)
         self.size = int(self.size)
      except (IOError, ValueError):
         self.size = size
         self.width = width

         with open(self.fileName, 'wb') as f:
            f.write(str(self.size).ljust(self.width - 1) + '\n')
            f.write((' '.ljust(self.width - 1) + '\n') * self.size)
            #for i in xrange(self.size):
            #   f.write((' '.ljust(self.width - 1) + '\n'))

   def __getitem__(self, key):
      h = (hash(key) % self.size) + 1
      with open(self.fileName, 'rb') as f:
         f.seek((h-1) * self.width)
         output = f.read(self.width)
      return output.strip()

   def __setitem__(self, key, value):
      h = (hash(key) % self.size) + 1
      with open(self.fileName, 'r+b') as f:
         f.seek((h-1) * self.width, 0)
         f.write(str(value).ljust(self.width - 1) + '\n')

if __name__ == '__main__':
   hd = hashDict('test.txt')
   print '%r %r %r' % (hd['apple'], hd['123'], hd[123])
   #hd['apple'] = 17
   #hd['123'] = 'abcde'
   #hd[123] = '1234'
   
   