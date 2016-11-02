import time
# if not installed already, run python -m pip install requests OR 
# pip install requests, whatever you normally do
import requests 
import random
import json

import bommerGame

practice = True

if practice:
    url = 'http://upe21.cs.rpi.edu:3000/api/games/practice'
else:
    url = 'http://upe21.cs.rpi.edu:3000/api/games/search'

with open('userinfo.json') as f:
    userInfo = json.load(f)

# search for new game
r = requests.post(url, data=userInfo) 

# when request comes back, that means you've found a match! (validation if server goes down?)
json = r.json()
print(json)
gameID = json['gameID']
playerID = json['playerID']
print(gameID)
print(playerID)
possibleMoves = ['mu', 'ml', 'mr', 'md', 'tu', 'tl', 'tr', 'td', 
                 'b', '', 'op', 'bp', 'buy_count', 'buy_range', 'buy_pierce', 'buy_block']

game = bommerGame.BommerGame()


while True:
    randomInt = random.randint(0,len(possibleMoves)-1)

    # submit sample move
    r = requests.post('http://upe21.cs.rpi.edu:3000/api/games/submit/' + gameID, 
                      data={'playerID': playerID, 'move': possibleMoves[randomInt], 
                            'devkey': userInfo["devkey"]}) 

    game.update(r.json())

    if not game:
        break

    #json = r.json()
    #print(json)
    #print()
    #output = json
