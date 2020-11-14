# Testing module for 328p_inteface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE

from Engine.gameState import GameState as gs
interface = __import__('328p_interface')

currentGamestate = gs()  # Instantiate test gamestate
move = 'a1h8'

interface.make_physical_move(currentGamestate, move)
