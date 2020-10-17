"""
-------------------------------
IMPORTS
-------------------------------
"""
import multiprocessing as mp
import time

from lichess import lichessInterface_new as interface

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

		self.eventProcess = mp.Process(target = interface.create_eventstream, args = self.eventStreamControlQueue)
		

