import time
# if not installed already, run python -m pip install requests OR 
# pip install requests, whatever you normally do
import requests 
import random
import json

import bommerGame

practice = True
numGames = 30000

#domain = 'http://upe21.cs.rpi.edu:3000'
domain = 'http://aicomp.io'

if practice:
    url = '%s/api/games/practice' % domain
else:
    url = '%s/api/games/search' % domain

with open('userinfo.json') as f:
    userInfo = json.load(f)



for i in xrange(numGames):
    print
    print 'Game %s' % i
    # search for new game
    print userInfo
    r = requests.post(url, data=userInfo) 
    
    # when request comes back, that means you've found a match! (validation if server goes down?)
    json = r.json()
    #print(json)
    gameID = json['gameID']
    playerID = json['playerID']
    print(gameID)
    print(playerID)
    possibleMoves = ['mu', 'ml', 'mr', 'md', 'tu', 'tl', 'tr', 'td', 
                     'b', '', 'op', 'bp', 'buy_count', 'buy_range', 'buy_pierce', 'buy_block']
    
    r = requests.post(('%s/api/games/submit/' % domain) + gameID, 
                          data={'playerID': playerID, 'devkey': userInfo["devkey"]})
    
    game = bommerGame.BommerGame(r.json())
    
    
    while True:
    
        # submit sample move
        r = requests.post(('%s/api/games/submit/' % domain) + gameID, 
                          data={'playerID': playerID, 'move': game.qlearn('qvalues_small.dat'), 
                                'devkey': userInfo["devkey"]}) 
    
        #print bool(game)
        
    
        #print r.json()
        try:
            game.update(r.json())
            if r.json()[u'state'] != 'in progress':
                game.qlearn('qvalues.dat')
                break                
        except (ValueError, TypeError):
            pass
    
        #json = r.json()
        #print(json)
        #print()
        #output = json
