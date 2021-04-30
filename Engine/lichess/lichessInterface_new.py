"""
-------------------------------
IMPORTS
-------------------------------
"""
import requests, time, json, os

#import settings

from Engine.lichess import settings
from Engine import chessboard, gui_pages as pages

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
def create_gamestream(gameid=""):
	if gameid == "":
		gameid = open('gameid.txt', 'r').read()
	response = requests.get('https://lichess.org/api/board/game/stream/{}'.format(gameid), headers={'Authorization': 'Bearer {}'.format(api_key)}, stream=True)
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
	    'color': kwargs["color"],
	}
	try:
		r = requests.post('https://lichess.org/api/challenge/' + username, json=configurations, 
						headers={'Authorization': 'Bearer {}'.format(api_key)})
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


""" challenge_cancel: cancel outgoing challenge
	params: 
		gameid - gameid that was generated from original challenge request
	return:
"""
def challenge_cancel(gameid):
	try:
		response = requests.post("https://lichess.org/api/challenge/{challengeId}/cancel".format(challengeId=gameid), headers={'Authorization': 'Bearer {}'.format(api_key)})
		return 1
	except:
		print("Unable ot cancel challenge")


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
def make_move(move):
	try:
		gameid = open('gameid.txt', 'r')
		r = requests.post('https://lichess.org/api/board/game/{id}/move/{move}'.format(id=gameid.read(), move=move), headers={'Authorization': 'Bearer {}'.format(api_key)})
		gameid.close()
		if r.ok:
			return 1
		# error code 400; return error message from LiChess
		else:
			print(r.content)
			return r.content
	except:
		pass


""" 
"""
def get_ongoing_games():
	r = requests.get('https://lichess.org/api/account/playing', headers={'Authorization': 'Bearer {}'.format(api_key)})
	lines = r.iter_lines()
    
	#iterate through the response message
	for line in lines:

	    if line:
	        event = json.loads(line.decode('utf-8'))
	        print(event['nowPlaying'], len(event['nowPlaying']))


"""
get all previously played games by user
params:
return:
	games - array of games with 
"""
def get_all_games():
	games = []
	r = requests.get('https://lichess.org/api/games/user/{username}'.format(username=pages.app_username), params={'max': 25},
					 headers={'Accept': 'application/x-ndjson', 'Authorization': 'Bearer {}'.format(api_key)})
	lines = r.iter_lines()
	for line in lines:
		event = json.loads(line.decode('utf-8'))
		
		gameid = event['id']
		creationTime = event['createdAt']
		white = event['players']['white']['user']['name']
		black = event['players']['black']['user']['name']

		games.append({'gameid':gameid, 'time':creationTime, 'white':white, 'black':black})

	return games		


""" game_over: either abort or resign
	params:
		option: either abort or resign
	return:
		1: game successfully aborted
		0: game successfully resigned
		-1: error
"""
def gameover(option, screen):
	gameid = open('gameid.txt', 'r')
	try:
		if option == "abort":
			# send abort message
			r = requests.post('https://lichess.org/api/board/game/{gameId}/abort'.format(gameId=gameid.read()), headers={'Authorization': 'Bearer {}'.format(api_key)})

		elif option == "resign":  
			# send resign message
			r = requests.post('https://lichess.org/api/board/game/{gameId}/resign'.format(gameId=gameid.read()),  headers={'Authorization': 'Bearer {}'.format(api_key)})

		gameid.close()
		return 1

	except:
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
