# 9/13/2020
# Test interface to initiate a game between local host and opponent

import time
import requests
import json

api_key = '2tQ0zLiWpJSSsF89'

# r = requests.get('https://lichess.org/api/account', auth=('user', 'pass'))
# I dont know how to add header with requests api (curl -H)

# r = requests.get('https://lichess.org/api/application/x-www-form-urlencoded', headers={'Authorization': 'Bearer {}'.format(api_key)})
# print(r.content)

# r = requests.post('https://lichess.org/api/board/seek',params={"time": [15], "increment": [0]}, headers={'Authorization': 'Bearer {}'.format(api_key)})

payload = {
    'time': 15,
    'increment': 0,
}

r = requests.post('https://lichess.org/api/challenge/weishanli', json=payload, headers={'Authorization': 'Bearer {}'.format(api_key)})
json_response = r.json()
print(json_response["challenge"]["id"])
gameid = json_response["challenge"]["id"]

time.sleep(10)

r2 = requests.post('https://lichess.org/api/board/game/{id}/move/{move}'.format(id=gameid, move="d2d4"), headers={'Authorization': 'Bearer {}'.format(api_key)})
print(r2.content)
# r2 = requests.get('https://lichess.org/api/board/game/stream/{}'.format(gameid), headers={'Authorization': 'Bearer {}'.format(api_key)})
# print(r2.content)

# Tue, 05 May 2020 09:59:16 GMT - Board Stream - {"id":"4YMxKQOF","variant":{"key":"standard","name":"Standard","short":"Std"},"clock":{"initial":3600000,"increment":10000},"speed":"classical","perf":{"name":"Classical"},"rated":false,"createdAt":1588672752766,"white":{"aiLevel":1},"black":{"id":"milesarmstrong","name":"milesarmstrong","title":null,"rating":1500,"provisional":true},"initialFen":"startpos","type":"gameFull","state":{"type":"gameState","moves":"e2e4","wtime":3600000,"btime":3600000,"winc":10000,"binc":10000,"wdraw":false,"bdraw":false,"status":"started"}}

