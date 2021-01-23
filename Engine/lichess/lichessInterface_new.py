"""
-------------------------------
IMPORTS
-------------------------------
"""
import requests, time, json, os

from Engine.lichess import settings
from Engine import chessboard

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
def create_gamestream():
	gameid = open('gameid.txt', 'r')
	response = requests.get('https://lichess.org/api/board/game/stream/{}'.format(gameid.read()), headers={'Authorization': 'Bearer {}'.format(api_key)}, stream=True)
	gameid.close()
	return response
			




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
	    'color': 'white',
	}
	try:
		r = requests.post('https://lichess.org/api/challenge/' + username, json=configurations, headers={'Authorization': 'Bearer {}'.format(api_key)})
		# check for successful challenge response
		if r.status_code == 200:

			# response message from challenge request to LiChess
			json_response = r.json()
			gameid = json_response["challenge"]["id"]
			return gameid

		# user was not found
		else:
			return 0
	except:
		print("Problem with challenge")





""" create_seek: start a seek for random opponent
	params:
	return:
"""
def create_seek():
	response = request.post('https://lichess.org/api/board/seek', headers={'Authorization': 'Bearer {}'.format(api_key)})
	return



""" make_move: request to make move to lichess server
	params:
	return:
"""
def make_move(move, screen):
	gameid = open('gameid.txt', 'r')
	r = requests.post('https://lichess.org/api/board/game/{id}/move/{move}'.format(id=gameid.read(), move=move), headers={'Authorization': 'Bearer {}'.format(api_key)})
	gameid.close()
	if r.ok:
		chessboard.display_alert(screen, "Okay")
		return 1
	# error code 400
	else:
		chessboard.display_alert(screen, r.content)
		return 0



""" game_over: either abort or resign
	params:
		option: either abort or resign
	return:
		1: game successfully aborted
		0: game successfully resigned
		-1: error
"""
def gameover(option):
	gameid = open('gameid.txt', 'r')
	try:
		if option == "abort":
			# send abort message
			r = request.post('https://lichess.org/api/board/game/{gameId}/abort'.format(gameId=gameid.read()), headers={'Authorization': 'Bearer {}'.format(api_key)})

		elif option == "resign":
			# send resign message
			r = request.post('https://lichess.org/api/board/game/{gameId}/resign'.format(gameId=gameid.read()), headers={'Authorization': 'Bearer {}'.format(api_key)})

		gameid.close()
		return 1

	except:
		print("Unable to complete, request issue")
		return 0



""" change_gameid
	params:
		gameid - new game id
	return:
"""
def change_gameid(gameid):
	file1 = open("gameid.txt", "w")
	file1.write(gameid)
	file1.close()
