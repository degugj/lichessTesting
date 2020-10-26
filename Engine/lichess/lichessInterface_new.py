"""
-------------------------------
IMPORTS
-------------------------------
"""
import requests, time, json, os

from Engine.lichess import settings

"""
-------------------------------
VARIABLES
-------------------------------
"""
api_key = settings.api_key

"""
-------------------------------
LICHESS API FUNCTIONS
-------------------------------
"""

""" get_accountinfo: get account info of desired user
	params:
		user - username
		password - password
	return:
		r.content
"""
def get_accountinfo(user, password):
	r = requests.get('https://lichess.org/api/account', auth=(user, password))
	return r.content




""" create_eventstream: creating an event stream using the API key (run this as a seperate process)
	params: 
		controlQueue
	return:
"""
def create_eventstream():
	response = requests.get('https://lichess.org/api/stream/event', headers={'Authorization': 'Bearer {}'.format(api_key)}, stream=True)
	return response




""" create_gamestream: creating an game stream using the gameid (run this as a seperate process)
	params:
		gameEventsQueue
	return:
"""
def create_gamestream(gameQueue):
	while 1:
		try:
			gameid = open('game.txt', 'r')
			# api call to start a game stream
			response = requests.get('https://lichess.org/api/board/game/stream/{}'.format(gameid.read()), headers={'Authorization': 'Bearer {}'.format(api_key)})
			lines = response.iter_lines()
			# iterate through the response message
			for line in lines:
				# place response events in control queue
				if line:
					event = json.loads(line.decode('utf-8'))
					print(event)
					gameQueue.put_nowait(event)
				else:
					gameQueue.put_nowait({"type": "ping"})

		except:
			pass




""" challenge_user
	params:
		username - name of player to challenge in LiChess server
		**kwargs - parameters for match configurations
	return:
		gameid - id of game created challenge request
"""
def challenge_user(username, **kwargs):

	# match configurations
	configurations = {     
	    'time': 15,
	    'increment': 0, 
	}
	r = requests.post('https://lichess.org/api/challenge/' + username, json=configurations, headers={'Authorization': 'Bearer {}'.format(api_key)})
	print(r.content)
	if r.status_code == 200:

		# response message from challenge request to LiChess
		json_response = r.json()
		gameid = json_response["challenge"]["id"]
		return gameid

	# user was not found
	else:
		return 0




""" make_move: request to make move to lichess server
	params:
	return:
"""
def make_move(move):
	gameid = open('gameid.txt', 'r')
	r = requests.post('https://lichess.org/api/board/game/{id}/move/{move}'.format(id=gameid.read(), move=move), headers={'Authorization': 'Bearer {}'.format(api_key)})
	if r.status_code == '200':
		print('status code 200')
		return (r.content, 1)
	# error code 400
	else:
		return (r.content, 0)




""" change_gameid
	params:
		gameid - new game id
	return:
"""
def change_gameid(gameid):
	file1 = open("gameid.txt", "w")
	file1.write(gameid)
	file1.close()
