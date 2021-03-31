# Testing module for 328p_fs_interface.py integration
import numpy as np
#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE
import importlib
from Engine.gameState import GameState as gs
#from Engine.x328p_interface import *
from Engine.x328p_interface import x328p_fs_interface as interface
# interface = importlib.import_module('.x328p_interface.x328p_fs_interface', 'Engine')
import time

currentGamestate = gs()  # Instantiate test gamestate

#print(currentGamestate.board)
# Reset the board to no pieces (as Sam has no pieces)
for indexR, row in enumerate(currentGamestate.board):
    for indexC, item in enumerate(row):
        currentGamestate.board[indexR][indexC] = '--'
        if indexR == 6 and indexC == 0:
            currentGamestate.board[indexR][indexC] = 'wP'
        if indexR == 6 and indexC == 1:
            currentGamestate.board[indexR][indexC] = 'wP'
        if indexR == 6 and indexC == 2:
            currentGamestate.board[indexR][indexC] = 'wP'
        if indexR == 6 and indexC == 3:
            currentGamestate.board[indexR][indexC] = 'wP'

#print(currentGamestate.board)

#interface.get_column(currentGamestate, 'a')
checkStatus = interface.initial_error_check(currentGamestate)
if checkStatus != 0:
    print("Waiting 5s to retry initial check...")
    time.sleep(5)
    checkStatus2 = interface.initial_error_check(currentGamestate)
    if checkStatus2 != 0:
        exit()
move = interface.start_fast_scan(currentGamestate)
print("Move resolved from Sam's subsystem:", move)

""""
messageNo1Init = interface.gamestateMessage(0b00001, 0b000, 0b11000011) # a2a3
messageNo2Init = interface.gamestateMessage(0b00010, 0b001, 0b11000001)
messageNo3Init = interface.gamestateMessage(0b00011, 0b010, 0b11000011)
messageNo4Init = interface.gamestateMessage(0b00100, 0b011, 0b11000011)
messageNo5Init = interface.gamestateMessage(0b00101, 0b100, 0b11010011)
messageNo6Init = interface.gamestateMessage(0b00110, 0b101, 0b11000011)
messageNo7Init = interface.gamestateMessage(0b00111, 0b110, 0b11000011)
messageNo8Init = interface.gamestateMessage(0b01000, 0b111, 0b11000011)

samState = [messageNo1Init, messageNo2Init, messageNo3Init, messageNo4Init,
            messageNo5Init, messageNo6Init, messageNo7Init, messageNo8Init]
newGs = np.array(currentGamestate.board)

#move = interface.resolve_chess_move(newGs, samState)
#print("Resolved Move:",move)
#interface.compare_chess_states(newGs, samState)

#interface.fast_scan_simulator_uart()
#interface.test_sim()


#messageNo1 = {'typ': 0b00000, 'col': 0b000, 'data': 0b00000000}

# messageNo0 = gamestateMessage(0b00000, 0b011, 0b00001000)
# #messageNo0.return_chess_cell()

# messageNo1 = gamestateMessage(0b00001, 0b101, 0b00000100)
# messageNo2 = gamestateMessage(0b00010, 0b111, 0b00010000)
# messageNo3 = gamestateMessage(0b00011, 0b011, 0b01000000)
# messageNo4 = gamestateMessage(0b00100, 0b001, 0b00001000)
# messageNo5 = gamestateMessage(0b00101, 0b000, 0b00000100)
# messageNo6 = gamestateMessage(0b00110, 0b100, 0b00000010)
# messageNo7 = gamestateMessage(0b00111, 0b110, 0b00000010)
# messageNo8 = gamestateMessage(0b01000, 0b011, 0b00010000)
# messageNo9 = gamestateMessage(0b01001, 0b010, 0b00000100)
# messageNo10 = gamestateMessage(0b01010, 0b110, 0b01000000)
# messageNo11 = gamestateMessage(0b01011, 0b011, 0b00100000)
# messageNo12 = gamestateMessage(0b01100, 0b111, 0b10000000)


"""
