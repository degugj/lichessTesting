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
def create_eventstream(controlQueue):
	while 1:
		try:
			# api call to start an event stream
			response = requests.get('https://lichess.org/api/stream/event', headers={'Authorization': 'Bearer {}'.format(settings.api_key)}, stream=True)

			lines = response.iter_lines()
			# iterate through the response message
			for line in lines:
				# place response events in control queue
				if line:
					event = json.loads(line.decode('utf-8'))
					print(event)
					controlQueue.put_nowait(event)
				else:
					controlQueue.put_nowait({"type": "ping"})
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
	r = requests.post('https://lichess.org/api/board/game/{id}/move/{move}'.format(id=settings.gameid, move=move), headers={'Authorization': 'Bearer {}'.format(api_key)})
	if r.status_code == '200':
		return
	# error code 400
	else:
		print("move is not valid")


""" change_gameid
	params:
		gameid - new game id
	return:
"""
def change_gameid(gameid):
	file1 = open("gameid.txt", "w")
	file1.write(gameid)
	file1.close()
