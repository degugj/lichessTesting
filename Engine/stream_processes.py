"""
-------------------------------
IMPORTS
-------------------------------
"""
import multiprocessing as mp
import time

from Engine.lichess import lichessInterface_new as interface

"""
-------------------------------
FUNCTIONS
-------------------------------
"""

""" 
EventStream
-Created after logging in to LiChess
-Side process that will update user on realtime events
	- gameStart, gameFinish, challenge, challengeCanceled, challengeDeclined
"""
class EventStream:
	def __init__(self):

		self.eventStreamManager = mp.Manager()
		self.eventStreamControlQueue = self.eventStreamManager.Queue()

		self.eventProcess = mp.Process(target = interface.create_eventstream, args = (self.eventStreamControlQueue,))
		self.eventProcess.start()

	def get_eventstreamProcess(self):
		return self.eventProcess

"""
GameStream
-Created after starting a game
-Side process that will update user on realtime game events

"""
class GameStream:
	def __init__(self):

		self.gameStreamManager = mp.Manager()
		self.gameStreamControlQueue = self.eventStreamManager.Queue()

		self.gameProcess = mp.Process(target = interface.create_gamestream, args = (self.gameStreamControlQueue,))
		self.gameProcess.start()
		