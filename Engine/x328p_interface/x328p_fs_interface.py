# Module and helper functions for interfacing with fast scanning 328P via I2C
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01
import numpy as np
letterToColumn = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

def print_gamestate(gs):
    newGs = np.array(gs.board)
    print(newGs)

def get_column(gs, columnChar):
    newGs = np.array(gs.board)
    print(newGs[:,letterToColumn[columnChar]])

def make_fast_scan(gs):
    return 0