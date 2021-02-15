# Testing module for 328p_fs_interface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE
import importlib
from Engine.gameState import GameState as gs
#from Engine.x328p_interface import *
interface = importlib.import_module('.x328p_interface.x328p_fs_interface', 'Engine')

currentGamestate = gs()  # Instantiate test gamestate

#interface.get_column(currentGamestate, 'a')
#interface.fast_scan_simulator()