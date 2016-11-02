
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

class Board:
    def __init__(size, hardBlockBoard, softBlockBoard, trailMap, bombMap, portalMap):
        pass

class BommerGame:
    def __init__(self, data):
        self.player =       Player(data[u'player'])
        self.opponent =     Player(data[u'opponent'])
        self.board =        Board(size = data[u'boardSize'], 
                                hardBlockBoard = data[u'hardBlockBoard'], 
                                softBlockBoard = data[u'softBlockBoard'],
                                trailMap = data[u'trailMap'], 
                                bombMap = data[u'bombMap'],
                                portalMap = data[u'portalMap'])

        self.state =        data[u'state']
        self.moveOrder =    data[u'moveOrder']
        self.playerIndex =  data[u'playerIndex']
        self.gameID =       data[u'gameID']
        self.moveIterator = data[u'moveIterator']
        self.playerID =     data[u'playerID']

    def __bool__(self):
        '''
        Returns true iff the game is in progress
        '''
        return self.state != 'complete'

    def ended(self):
        return self.state == 'complete'
