"""
-------------------------------
IMPORTS
-------------------------------
"""
import requests, time, json, os

import settings

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


""" change_gameid
params:
	gameid - new game id
return:
	no return
"""
def change_gameid(gameid):
	file1 = open("gameid.txt", "w")
	file1.write(gameid)
	file1.close()
	return

