# Module and helper functions for interfacing with Atmega328p via Pi UART
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01

letterToColumn = {'a':6, 'b':8,'c':10,'d':12,'e':14,'f':16,'g':18,'h':20}  # To translate cell to posMap location
# easy translation from number to row ((number * 2) + 1)

# self.letter_to_x = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
# self.number_to_y = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}

# Translates an 8x8 gamestate to a 24x24 piece position map
def gamestate_to_position_map(gamestate):
    posMap = [['. ']*27 for _ in range(17)]

    # TODO add buffer translations
    for i in range(8):
        for j in range(8):
            posI = (i*2)+1
            posJ = (j*2)+1
            # print(gamestate.board[i][j])
            if(gamestate.board[i][j] != "--"):
                posMap[16 - posI][posJ+5] = gamestate.board[i][j]
            else:
                posMap[posI][posJ + 5] = '. '
    return posMap


# Creates a heuristic map of weights equal to the distance from the destination position
def create_heuristic_map(endPos):
    heurMap = [[0]*27]*25
    return 0


# Returns the Astar path of
def find_astar_path(posMap, heurMap, startPos, endPos):
    return 0


# Sends 328P a path via UART
def send_to_328p(path):
    return 0

def print_posMap(map):
    print("\tBlack \t\t\t\t\t\t\t\tBoard \t\t\t\t\t\t\tWhite")
    for i in range(16, -1, -1):
        for j in range(4, -1, -1):
            print(map[i][j], end=' ')
        print("\t", end = '')
        for x in range(16, -1, -1):
            print(map[i][5 + x], end=' ')
        print("\t", end = '')
        for j in range(4, -1, -1):
            print(map[i][22 + j], end=' ')
        print("\t")



# External function used to interface with GUI and game execution. Takes current gamestate and string move (ie 'e4e5')
def make_physical_move(gamestate, move, capturedPiece=None):
    # TODO Extract and interpret move as start and end pos
    # TODO Call gamestate_to_position_map()
    # TODO Call create_heuristic_map()
    # TODO Call find_astar_path() using the arguments obtained above
    # TODO Call send_to_328P() with path returned above

    # TODO Figure out UART, logic analyzer and returns for Wei
    return 0
