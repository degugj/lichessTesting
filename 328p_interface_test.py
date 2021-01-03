# Testing module for 328p_inteface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE
import importlib
from Engine.gameState import GameState as gs
#from Engine.328p_interface import *
interface = importlib.import_module('.328p_interface.328p_interface', 'Engine')

currentGamestate = gs()  # Instantiate test gamestate
move = 'a6h6'

interface.make_physical_move(currentGamestate, move)
