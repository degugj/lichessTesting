# Testing module for 328p_fs_interface.py integration

#  WARNING: TEST WILL NOT WORK WITHOUT MODIFICATION TO GAMESTATE. CONSTRUCTOR MUST SUPPORT NONE FOR GAMEQUEUE
import importlib
from Engine.gameState import GameState as gs
#from Engine.x328p_interface import *
from Engine.x328p_interface.x328p_fs_interface import gamestateMessage
interface = importlib.import_module('.x328p_interface.x328p_fs_interface', 'Engine')


currentGamestate = gs()  # Instantiate test gamestate

#interface.get_column(currentGamestate, 'a')
#interface.fast_scan_simulator_uart()
#interface.test_sim()


#messageNo1 = {'typ': 0b00000, 'col': 0b000, 'data': 0b00000000}

messageNo0 = gamestateMessage(0b00000, 0b011, 0b00001000)
messageNo0.return_chess_cell()

messageNo1 = gamestateMessage(0b00001, 0b101, 0b00000100)
messageNo2 = gamestateMessage(0b00010, 0b111, 0b00010000)
messageNo3 = gamestateMessage(0b00011, 0b011, 0b01000000)
messageNo4 = gamestateMessage(0b00100, 0b001, 0b00001000)
messageNo5 = gamestateMessage(0b00101, 0b000, 0b00000100)
messageNo6 = gamestateMessage(0b00110, 0b100, 0b00000010)
messageNo7 = gamestateMessage(0b00111, 0b110, 0b00000010)
messageNo8 = gamestateMessage(0b01000, 0b011, 0b00010000)
messageNo9 = gamestateMessage(0b01001, 0b010, 0b00000100)
messageNo10 = gamestateMessage(0b01010, 0b110, 0b01000000)
messageNo11 = gamestateMessage(0b01011, 0b011, 0b00100000)
messageNo12 = gamestateMessage(0b01100, 0b111, 0b10000000)



