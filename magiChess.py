# 9/13/2020
# Test interface to initiate a game between local host and opponent

import time
import requests
import json
import settings
import os
import multiprocessing


api_key = settings.api_key

def get_event_stream(controlQueue):
    while 1:
        time.sleep(1)
        print("hello")
        try:
            response = requests.get('https://lichess.org/api/stream/event', headers={'Authorization': 'Bearer {}'.format(settings.api_key)}, stream=True)
            lines = response.iter_lines()
            for line in lines:
                if line:
                    print(line)
                    event = json.loads(line.decode('utf-8'))
                    print(event)
                    controlQueue.put_nowait(event)
                else:
                    controlQueue.put_nowait({"type": "ping"})
        except:
            pass

def get_game_stream(gameId):
    return requests.get('https://lichess.org/api/board/game/stream/{}'.format(settings.gameid), headers={'Authorization': 'Bearer {}'.format(settings.api_key)})

def challenge_wei():
    payload = {     # Match configuration
        'time': 15,
        'increment': 0,
    }

    return requests.post('https://lichess.org/api/challenge/weishanli', json=payload, headers={'Authorization': 'Bearer {}'.format(settings.api_key)})  # Challenges Wei to a match


def main():
    manager = multiprocessing.Manager()
    controlQueue = manager.Queue()
    streamEventProcess = multiprocessing.Process(target=get_event_stream, args=(controlQueue,))
    streamEventProcess.start()

    event = controlQueue.get()
    time.sleep(1)
    challenge_wei()

    time.sleep(10)
if __name__ == "__main__":
    main()
