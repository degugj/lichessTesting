import requests
import time
import settings


gameFound = 0
while not gameFound:
    file1 = open("gameid.txt", "r")
    gameid = file1.read()
    file1.close()
    print("Game ID: |", gameid, "|")
    r2 = requests.get('https://lichess.org/api/board/game/stream/{}'.format(settings.gameid), headers={'Authorization': 'Bearer {}'.format(settings.api_key)})
    print(r2.status_code)
    if r2.status_code == '200':
        gameFound = 1
    print(r2.content)
    print(r2.reason)
    time.sleep(2)

print("Game Found")
