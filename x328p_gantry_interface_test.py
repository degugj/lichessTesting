# Testing module for 328p_inteface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE
import importlib
from Engine.gameState import GameState as gs
#from Engine.x328p_interface import *
interface = importlib.import_module('.x328p_interface.x328p_gantry_interface', 'Engine')

currentGamestate = gs()  # Instantiate test gamestate
move = 'h8a1'
currentGamestate.wBuffer[0][0] = 'wP'
currentGamestate.wBuffer[0][1] = 'wP'
currentGamestate.wBuffer[1][0] = 'wP'
currentGamestate.wBuffer[1][1] = 'wP'
currentGamestate.wBuffer[2][0] = 'wP'

currentGamestate.bBuffer[0][0] = 'bP'
currentGamestate.bBuffer[0][1] = 'bP'
currentGamestate.bBuffer[1][0] = 'bP'
currentGamestate.bBuffer[1][1] = 'bP'
currentGamestate.bBuffer[2][0] = 'bP'

interface.make_physical_move(currentGamestate, move)
#interface.transmit_uart_sim()
