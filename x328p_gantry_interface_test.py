# Testing module for 328p_inteface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE
import importlib
from Engine.gameState import GameState as gs
import numpy as np
#from Engine.x328p_interface import *
interface = importlib.import_module('.x328p_interface.x328p_gantry_interface', 'Engine')

currentGamestate = gs()  # Instantiate test gamestate
# move = 'h8a1'
# currentGamestate.wBuffer[0][0] = 'wP'
# currentGamestate.wBuffer[0][1] = 'wP'
# currentGamestate.wBuffer[1][0] = 'wP'
# currentGamestate.wBuffer[1][1] = 'wP'
# currentGamestate.bBuffer[0][0] = 'bP'
# currentGamestate.bBuffer[0][1] = 'bP'
# currentGamestate.bBuffer[1][0] = 'bP'
# currentGamestate.bBuffer[1][1] = 'bP'

# gameRecord = ['d4e5','e4d5','f4f5','g3f4']
# for move in gameRecord:
#     print(np.array(currentGamestate.board))
#     currentGamestate.move_piece(move)
#     print(np.array(currentGamestate.board))
# currentGamestate.bBuffer[0][0] = 'bP'
# currentGamestate.bBuffer[0][1] = 'bP'
# currentGamestate.bBuffer[1][0] = 'bP'
# currentGamestate.bBuffer[1][1] = 'bP'
# currentGamestate.bBuffer[2][0] = 'bP'

# currentGamestate.board[7-6][7-2] = "wP"
# currentGamestate.board[7-5][7-2] = "bP"
# currentGamestate.board[7-6][7-3] = "--"
# currentGamestate.board[7-3][7-2] = "bP"
currentGamestate.board[7-6][7-3] = "--"
currentGamestate.board[7-6][7-4] = "--"
currentGamestate.board[7-1][7-1] = "--"
currentGamestate.board[7-1][7-2] = "--"
currentGamestate.board[7-1][7-3] = "--"
currentGamestate.board[7-1][7-4] = "--"
currentGamestate.board[7-1][7-7] = "--"
currentGamestate.board[7-2][7-1] = "wP"
currentGamestate.board[7-2][7-1] = "wP"
currentGamestate.board[7-3] = ["wP", "--","--","wP","wP","bP","--","--"]
currentGamestate.board[7-4][7-4] = "bP"
currentGamestate.board[7-4][7-2] = "wP"

#print(currentGamestate)
#print(currentGamestate.wBuffer)
# interface.make_physical_move(currentGamestate, 'f5e4')
#interface.make_physical_move(currentGamestate, 'f5e4')
interface.make_physical_state_congruent(currentGamestate, gs())

#interface.transmit_uart_sim()
