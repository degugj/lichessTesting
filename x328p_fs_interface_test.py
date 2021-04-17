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

# print(currentGamestate.board)
# Reset the board to no pieces (as Sam has no pieces)
for indexR, row in enumerate(currentGamestate.board):
    for indexC, item in enumerate(row):
        currentGamestate.board[indexR][indexC] = '--'
        if indexR == 6 and indexC == 4:
            currentGamestate.board[indexR][indexC] = 'wP'
        if indexR == 6 and indexC == 5:
            currentGamestate.board[indexR][indexC] = 'wP'
        #if indexR == 6 and indexC == 2:
        #    currentGamestate.board[indexR][indexC] = 'wP'
print("Initial State:")
print(np.array(currentGamestate.board))

#interface.get_column(currentGamestate, 'a')

checkStatus = interface.initial_error_check(currentGamestate)
if checkStatus == 0:
    while True:
            move = interface.start_fast_scan(currentGamestate)
            print("Move resolved from Sam's subsystem:", move)
            if move == -1:
                break
            currentGamestate.move_piece(move)
            print("State after sensed physical move\n")
            print(currentGamestate.board)
""""
while True:
    checkStatus = interface.initial_error_check(currentGamestate)
    if checkStatus == 0:
        move = interface.start_fast_scan(currentGamestate)
        print("Move resolved from Sam's subsystem:", move)
        if move == -1:
            break
    else:
        print("Retrying in 4 seconds..")
        time.sleep(4)
"""
    #print("Waiting 5s to retry initial check...")
    #time.sleep(5)
    #checkStatus2 = interface.initial_error_check(currentGamestate)
    #if checkStatus2 != 0:
    #    exit()






# messageNo1Init = interface.gamestateMessage(0b00001, 0b000, 0b11000011) # a2a3
# messageNo2Init = interface.gamestateMessage(0b00010, 0b001, 0b11000001)
# messageNo3Init = interface.gamestateMessage(0b00011, 0b010, 0b11000011)
# messageNo4Init = interface.gamestateMessage(0b00100, 0b011, 0b11000011)
# messageNo5Init = interface.gamestateMessage(0b00101, 0b100, 0b11010011)
# messageNo6Init = interface.gamestateMessage(0b00110, 0b101, 0b11000011)
# messageNo7Init = interface.gamestateMessage(0b00111, 0b110, 0b11000011)
# messageNo8Init = interface.gamestateMessage(0b01000, 0b111, 0b11000011)
#
# samState = [messageNo1Init, messageNo2Init, messageNo3Init, messageNo4Init,
#             messageNo5Init, messageNo6Init, messageNo7Init, messageNo8Init]
# newGs = np.array(currentGamestate.board)


# messageNo1Init = interface.gamestateMessage(0b00001, 0b000, 0b11000011)
# messageNo2Init = interface.gamestateMessage(0b00010, 0b001, 0b11000011)
# messageNo3Init = interface.gamestateMessage(0b00011, 0b010, 0b11000011)
# messageNo4Init = interface.gamestateMessage(0b00100, 0b011, 0b11000011)
# messageNo5Init = interface.gamestateMessage(0b00101, 0b100, 0b11000011)
# messageNo6Init = interface.gamestateMessage(0b00110, 0b101, 0b11000011)
# messageNo7Init = interface.gamestateMessage(0b00111, 0b110, 0b11000011)
# messageNo8Init = interface.gamestateMessage(0b01000, 0b111, 0b11000011)
#
# messageNo1InitB = interface.gamestateMessage(0b00001, 0b000, 0b11000011)
# messageNo2InitB = interface.gamestateMessage(0b00010, 0b001, 0b11000011)
# messageNo3InitB = interface.gamestateMessage(0b00011, 0b010, 0b11000001)
# messageNo4InitB = interface.gamestateMessage(0b00100, 0b011, 0b11000011)
# messageNo5InitB = interface.gamestateMessage(0b00101, 0b100, 0b11000011)
# messageNo6InitB = interface.gamestateMessage(0b00110, 0b101, 0b11000011)
# messageNo7InitB = interface.gamestateMessage(0b00111, 0b110, 0b11000011)
# messageNo8InitB = interface.gamestateMessage(0b01000, 0b111, 0b11000011)
#
# messageNo1InitC = interface.gamestateMessage(0b00001, 0b000, 0b11000011)
# messageNo2InitC = interface.gamestateMessage(0b00010, 0b001, 0b10000011)
# messageNo3InitC = interface.gamestateMessage(0b00011, 0b010, 0b11000001)
# messageNo4InitC = interface.gamestateMessage(0b00100, 0b011, 0b11000011)
# messageNo5InitC = interface.gamestateMessage(0b00101, 0b100, 0b11000011)
# messageNo6InitC = interface.gamestateMessage(0b00110, 0b101, 0b11000011)
# messageNo7InitC = interface.gamestateMessage(0b00111, 0b110, 0b11000011)
# messageNo8InitC = interface.gamestateMessage(0b01000, 0b111, 0b11000011)
#
# messageNo1InitD = interface.gamestateMessage(0b00001, 0b000, 0b11000011)
# messageNo2InitD = interface.gamestateMessage(0b00010, 0b001, 0b10000011)
# messageNo3InitD = interface.gamestateMessage(0b00011, 0b010, 0b11000011)
# messageNo4InitD = interface.gamestateMessage(0b00100, 0b011, 0b11000011)
# messageNo5InitD = interface.gamestateMessage(0b00101, 0b100, 0b11000011)
# messageNo6InitD = interface.gamestateMessage(0b00110, 0b101, 0b11000011)
# messageNo7InitD = interface.gamestateMessage(0b00111, 0b110, 0b11000011)
# messageNo8InitD = interface.gamestateMessage(0b01000, 0b111, 0b11000011)
#
# samStateConstant = [messageNo1Init, messageNo2Init, messageNo3Init, messageNo4Init,
#             messageNo5Init, messageNo6Init, messageNo7Init, messageNo8Init]
#
# samStateB = [messageNo1InitB, messageNo2InitB, messageNo3InitB, messageNo4InitB,
#             messageNo5InitB, messageNo6InitB, messageNo7InitB, messageNo8InitB]
#
# samStateC = [messageNo1InitC, messageNo2InitC, messageNo3InitC, messageNo4InitC,
#             messageNo5InitC, messageNo6InitC, messageNo7InitC, messageNo8InitC]
#
# samStateD = [messageNo1InitD, messageNo2InitD, messageNo3InitD, messageNo4InitD,
#             messageNo5InitD, messageNo6InitD, messageNo7InitD, messageNo8InitD]
#
#
# messageStates = [samStateConstant, samStateB, samStateC, samStateD]
# newGs = np.array(currentGamestate.board)
#
#
# #move = interface.resolve_chess_move_v2(newGs, samStateB, samStateC)
#
# isMoveNotFound = True
# samState = None
# prevSamState = None
# startCell = None
# destCell = None
# for state in messageStates:
#     # First one is compared to local gs
#     samState = state
#     print(state)
#     time.sleep(3)
#     if startCell is None or startCell == -1:  # Check this OR condition
#         startCell = interface.find_start_cell(newGs, samState)
#         print("startCell:",startCell)
#         if startCell != -1 and startCell[1][0] != currentGamestate.userColor:
#
#             startCell = -1
#     else:
#         #print("else")
#         # Finesse for testing the move resolution
#         # samState2[7].data = 0b11000101
#         destCell = interface.resolve_chess_move_v2(newGs, samState, prevSamState)
#         # unsure about a check here
#         print("destCell",destCell)
#         if destCell != -1 and startCell != -1 and destCell == startCell: # User changed move
#             print("User placed piece back. Continue making move.")
#             startCell = -1
#             destCell = -1
#
#         if destCell != -1 and startCell != -1 and destCell != startCell:
#             # Transmit Stop
#             isMoveNotFound = False
#             # Serial write stop message to Sam
#             #transmission_byte0 = 0b00111000
#             #interface.send_to_328p(transmission_byte0, "Stop Fast Scan")
#             print("Move:",startCell[0] + destCell[0])
#
#     prevSamState = samState.copy()





# >>>>>>> Stashed changes
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



