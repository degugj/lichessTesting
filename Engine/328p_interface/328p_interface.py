# Module and helper functions for interfacing with Atmega328p via Pi UART
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01

letterToColumn = {}  # To translate cell to posMap location
numberToRow = {}

# self.letter_to_x = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
# self.number_to_y = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}

# Translates an 8x8 gamestate to a 24x24 piece position map
def gamestate_to_position_map(gamestate):
    posMap = [[0]*24]*24
    return gamestate


# Creates a heuristic map of weights equal to the distance from the destination position
def create_heuristic_map(endPos):
    heurMap = [[0]*24]*24
    return 0


# Returns the Astar path of
def find_astar_path(posMap, heurMap, startPos, endPos):
    return 0


# Sends 328P a path via UART
def send_to_328p(path):
    return 0


# External function used to interface with GUI and game execution. Takes current gamestate and string move (ie 'e4e5')
def make_physical_move(gamestate, move, capturedPiece=None):
    # TODO Extract and interpret move as start and end pos
    # TODO Call gamestate_to_position_map()
    # TODO Call create_heuristic_map()
    # TODO Call find_astar_path() using the arguments obtained above
    # TODO Call send_to_328P() with path returned above

    # TODO Figure out UART, logic analyzer and returns for Wei
    return 0
