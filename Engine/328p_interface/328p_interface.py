# Module and helper functions for interfacing with Atmega328p via Pi UART
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01

import math
import heapq
import serial
import time
import sys
letterToColumn = {'a':3, 'b':7,'c':9,'d':11,'e':13,'f':15,'g':17,'h':19}  # To translate cell to posMap location
# easy translation from number to row ((number * 2) + 1)

# self.letter_to_x = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
# self.number_to_y = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
message_types = {'XADDRESS':0b00011111, 'YADDRESS':0b00111111, 'RFID':0b01011111, 'EM':0b01111111, 'GO':0b10011111, 'ARRIVED':10111111,'ELSE':11011111}

class Node:
    def __init__(self, state='. ', parent=None, pos=[0, 0]):
        self.state = state      # Value
        self.parent = parent    # parent node
        self.heuristic = math.inf
        self.pos = pos
        self.cost = 0
        self.isGoal = 0
        self.costCreated = 0

    def successors(self, map):
        succs = []
        x = self.pos[0]
        y = self.pos[1]

        if y-1 >= 0:
            child = map[self.pos[0]][self.pos[1]-1]
            succs.append(child)

        if x - 1 >= 0:
            child = map[self.pos[0]-1][self.pos[1]]
            succs.append(child)

        if y - 1 >= 0 and x - 1 >= 0:
            child = map[self.pos[0]-1][self.pos[1]-1]
            succs.append(child)

        if y + 1 <= 26:
            child = map[self.pos[0]][self.pos[1]+1]
            succs.append(child)

        if x + 1 <= 16:
            child = map[self.pos[0]+1][self.pos[1]]
            succs.append(child)

        if x + 1 <= 16 and y + 1 <= 26:
            child = map[self.pos[0]+1][self.pos[1]+1]
            succs.append(child)

        if x + 1 <= 16 and y - 1 >= 0:
            child = map[self.pos[0]+1][self.pos[1]-1]
            succs.append(child)

        if x - 1 >= 0 and y + 1 <= 26:
            child = map[self.pos[0]-1][self.pos[1]+1]
            succs.append(child)

        return succs

    def __str__(self):
        # if self.isGoal:
        #     return " G  "
        # if self.heuristic == math.inf:
        #     return "null"
        # else:
        #     if len(str(self.heuristic)) == 3:
        #         return str(self.state)[0:4] + " "
        #     else:
        #         return str(self.state)[0:4]
        return self.state



# Translates an 8x8 gamestate to a 24x24 piece position map
def gamestate_to_position_map(gamestate):
    posMap = [[Node() for _ in range(25)] for _ in range(17)]
    for i in range(len(posMap)):
        for j in range(len(posMap[i])):
            posMap[i][j].pos = [i, j]
    # TODO add buffer translations
    for i in range(8):
        for j in range(8):
            posI = (i*2)+1
            posJ = (j*2)+1
            # print(gamestate.board[i][j])
            if(gamestate.board[i][j] != "--"):
                node = posMap[16 - posI][posJ+4]
                node.state = gamestate.board[i][j]
                node.pos = [16 - posI, posJ+4]
            else:
                posMap[posI][posJ + 5].state = '. '
    return posMap


# Creates a heuristic map of weights equal to the distance from the destination position
def create_heuristic_map(posMap, endPos):
    # posMap[endPos[0]][endPos[1]].heuristic = " G  "
    for i in range(len(posMap)):
        for j in range(len(posMap[i])):
            if posMap[i][j].state == '. ':
                straightLineDist = math.sqrt(math.pow(endPos[0]-i,2) + math.pow(endPos[1]-j, 2))
                posMap[i][j].heuristic = straightLineDist
            else:
                posMap[i][j].heuristic = math.inf
        # time.sleep(.7)
        # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        # print_posMap(posMap)
        # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    posMap[endPos[0]][endPos[1]].isGoal = 1
    # print(posMap[endPos[0]][endPos[1]].pos)
    return posMap


# Returns the Astar path of
def greedy(heurMap, startNode):
    # print(inputPuzzle.pretty())

    solution = []
    frontier = []
    explored = set()

    # solution.append(startNode)  # Start is first solution
    # heapq.heappush(frontier, (0,id(startNode),startNode))
    frontier.append(startNode)
    frontierCount = 1
    expandCount = 0

    if startNode.isGoal:
        return solution
    while len(frontier) != 0:
        node = heapq.heappop(frontier)
        solution.append(node)
        # time.sleep(1)
        # print_posMap(heurMap)
        # print("Checking: ", node.pos)
        # time.sleep(1)
        # print("Heur: ", node[1].heuristic)
        if node.isGoal:
            # tmpNode = node[2]
            # while tmpNode.parent is not None:
            #     solution.insert(1, tmpNode)
            #     print("Node added: ", tmpNode.pos)
            #     tmpNode = tmpNode.parent
            #     time.sleep(1)
            return solution

        explored.add(node)
        succ = node.successors(heurMap)
        # for i in succ:
        #     print(i.pos)
        expandCount += 1
        if expandCount >= 100000:
            # print("Search halted")
            return -1
        bestNode = Node()
        for n in succ:
            # print("Child: ", n.pos)
            if n.heuristic != math.inf and n not in explored:
                # print("Good to check")

                if bestNode.heuristic > n.heuristic:
                    # print("better heur node")
                    bestNode = n
            else:
                pass
                # print("skip child")
            if n.isGoal == 1:
                solution.append(n)
                return solution
        frontier.append(bestNode)
            # print(succ)
            # if n is not None:
            #     # print(n.pos)
            #     # print(n)
            #     if n.parent is not None:
            #         tmpCost = 1 + n.parent.cost
            #         if tmpCost < n.cost:
            #             n.cost = tmpCost
            #             n.parent = node[2]
            #         else:
            #             pass  # Cost created and new cost is not better. Dont update cost or rset parent
            #         # n.cost = 1 + n.parent.cost
            #         # n.parent = node[2]
            #         # n.costCreated = 1
            #     else:
            #         n.cost = 1

            # else:
            #     n.cost = 0
            # test = False
            # for i in frontier:
            #     if(i[2] == n):
            #         test = True
            # if not test and (n not in explored):
            #     # print("pos added: ",n.pos)
            #     heapq.heappush(frontier, (n.heuristic + n.cost,id(n), n))
            #     frontierCount += 1

    print("no solution")
    # print("path cost: N/A since no solution was found")
    print("frontier: " + str(frontierCount))
    print("expandCount: " + str(expandCount))
    return -1

# Returns an 8-bit address message
def message_encode(value, type):
    justValue = 0b11100000 | int(value)  # Populate hot bits in message type bits
    print(justValue& message_types[type])
    message = justValue& message_types[type]
    return message



# 328P UART conversation for controlling EM
def transmit_path(path):
    # ADD X (path[0])
    print("XADD Message: ",format(message_encode(path[0].pos[1],"XADDRESS"), '#010b'))
    #send_to_328p(bin(message_encode(path[0].pos[1],"XADDRESS")))
    # ADD Y
    print("YADD Message: ",format(message_encode(path[0].pos[0],"YADDRESS"), '#010b'))
    # GO
    print("GO Message: ",format(message_encode(0b11111,"GO")))
    # Wait for ARRIVED
    print("Wait for ARRIVED and gantry position (Mocking with sleep for now)")
    time.sleep(1)
    # Check RFID, compare to my state
    print("Recieve and confirm RFID (Mocking with sleep for now)")
    time.sleep(1)
    # EM ON
    print("EM Message: ",format(message_encode(0b11111,"EM"), '#010b'))
    # Loop path[1] and on:
    for i in path[1:len(path)]:
        print("XADD Message: ", format(message_encode(i.pos[1], "XADDRESS"), '#010b'))
        print("YADD Message: ", format(message_encode(i.pos[0], "YADDRESS"), '#010b'))
        print("GO Message: ", format(message_encode(i.pos[0], "GO"), '#010b'))

    #    ADD X
    #    ADD Y
    #    GO
    # EM OFF
    return

# Sends 328P a path via UART
def send_to_328p(data):
    
    ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
    #while True:
        #received_data = ser.read()  # read serial port
        #sleep(0.03)
        #data_left = ser.inWaiting()  # check for remaining byte
        #received_data += ser.read(data_left)
    print(data)  # print received data
    ser.write(data)  # transmit data serially
    
    #print("Solution Path:")
    #for i in path:
    #    print(i.pos)

    # Maybe use length to confirm path or some kind of checksum
    return 0

def print_posMap(map, path=None):
    if (path != None):
        for i in range(len(path)):
            solNode = path[i]
            map[solNode.pos[0]][solNode.pos[1]].state = u"\u26AA"
    print("\033[1m\tBlack \t\t\t\t\t\t\tBoard \t\t\t\t\t\tWhite")
    for i in range(16, -1, -1):
        for j in range(4):
            print(map[i][j], end=' ')
        print("\t", end = '')
        for x in range(17):
            print(map[i][4 + x], end=' ')
        print("\t", end = '')
        for j in range(4):
            print(map[i][21 + j], end=' ')
        print("\t")




# External function used to interface with GUI and game execution. Takes current gamestate and string move (ie 'e4e5')
def make_physical_move(gamestate, move, capturedPiece=None):
    # TODO Extract and interpret move as start and end pos
    posMap = gamestate_to_position_map(gamestate)  # convert 8x8 to position map
    # print("Move: ", move)
    # print("Position State: ")


    # print('')
    startPos = [0,0]
    startPos[0] = (int(move[1]) * 2) - 1
    startPos[1] = letterToColumn[move[0]]
    # print("Start Node: ", startPos, "(Cell: " + move[0:2] +")")
    # print("start: ", str(startPos))
    endPos = [0, 0]
    endPos[0] = (int(move[3:len(move)]) * 2) - 1
    # print(move[3:len(move)])
    endPos[1] = letterToColumn[move[2]]
    # print(endPos[1])
    # print("Goal Node: ", endPos, "(Cell: " + move[2:4] +")")

    heurMap = create_heuristic_map(posMap, endPos)
    # interface.print_posMap(heurMap)

    solution = greedy(heurMap, heurMap[startPos[0]][startPos[1]])
    # print("Path: ")
    print("Initial Position Map: ")
    print_posMap(posMap)
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print_posMap(heurMap, solution)
    # time.sleep(5)
    # for i in range(len(solution)):
    #     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #     solNode = solution[i]
    #     sys.stdout.write("\n\r{0}".format(str(i)))
    #     posMap[solNode.pos[0]][solNode.pos[1]].state = u"\u26AA"
    #     print_posMap(heurMap)
    #     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #     # sys.stdout.flush()
    #     time.sleep(1)
    # print("Sending path via UART...")
    # send_to_328p(solution)
    transmit_path(solution)
    # TODO Call gamestate_to_position_map()
    # TODO Call create_heuristic_map()
    # TODO Call find_astar_path() using the arguments obtained above
    # TODO Call send_to_328P() with path returned above

    # TODO Figure out UART, logic analyzer and returns for Wei
    return 0
