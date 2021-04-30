# Module and helper functions for interfacing with Atmega328p via Pi UART
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01

import math
import heapq
import serial
import time
import sys
letterToColumn = {'a':5, 'b':7,'c':9,'d':11,'e':13,'f':15,'g':17,'h':19}  # To translate cell to posMap location
pieceToBuffer = {'wP':[15,0], 'bP': [15, 24], 'bP': [15, 22]}
# easy translation from number to row ((number * 2) + 1)
ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate

# self.letter_to_x = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
# self.number_to_y = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
message_types = {'XADDRESS':0b00111111, 'YADDRESS':0b01011111, 'RFID':0b01111111, 'EM':0b10011111, 'GO':0b10111111, 'ARRIVED':0b11011111,'ELSE':11111111, 'BUSY':11100101}

currentGantryPos=[0,0]

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
            succs.append((child, 's'))

        if x - 1 >= 0:
            child = map[self.pos[0]-1][self.pos[1]]
            succs.append((child, 'w'))

        if y - 1 >= 0 and x - 1 >= 0:
            child = map[self.pos[0]-1][self.pos[1]-1]
            if map[self.pos[0] - 1][self.pos[1]].state == '. ' and map[self.pos[0]][self.pos[1] - 1].state == '. ':
                succs.append((child, 'sw'))

        if y + 1 <= 24:
            child = map[self.pos[0]][self.pos[1]+1]
            succs.append((child, 'n'))

        if x + 1 <= 16:
            child = map[self.pos[0]+1][self.pos[1]]
            succs.append((child, 'e'))

        if x + 1 <= 16 and y + 1 <= 24:
            child = map[self.pos[0]+1][self.pos[1]+1]
            if map[self.pos[0]+1][self.pos[1]].state == '. ' and map[self.pos[0]][self.pos[1]+1].state == '. ':
                print(map[self.pos[0]+1][self.pos[1]].state)
                succs.append((child, 'ne'))

        if x + 1 <= 16 and y - 1 >= 0:
            child = map[self.pos[0]+1][self.pos[1]-1]
            if map[self.pos[0]+1][self.pos[1]].state == '. ' and map[self.pos[0]][self.pos[1]-1].state == '. ':
                succs.append((child, 'nw'))

        if x - 1 >= 0 and y + 1 <= 24:
            child = map[self.pos[0]-1][self.pos[1]+1]
            if map[self.pos[0] - 1][self.pos[1]].state == '. ' and map[self.pos[0]][self.pos[1] + 1].state == '. ':
                succs.append((child, 'se'))

        return succs

    def __str__(self):
        return str(self.heuristic)

def next_buffer_pos(gamestate, piece):
    pieceColor = piece[0]
    # if captured piece is black
    if pieceColor == 'b':
        # check if captured piece is pawn
        if piece[1] == 'P':
            for row in range(4):
                for column in range(2):
                    if gamestate.bBuffer[row][column] == '--':
                        return [row, column]
        # all pieces other than pawn; bishop, knight, rook, queen
        else:
            for column in range(2):
                if gamestate.bBuffer[gamestate.bufferMap[piece[1]]][column] == '--':
                    return [gamestate.bufferMap[piece[1]], column]
    # if captured piece is white
    elif pieceColor == 'w':
        # check if captured piece is pawn, bishop, knight, rook, or queen and place into buffer accordingly
        if piece[1] == 'P':
            for row in range(4):
                for column in range(2):
                    if gamestate.wBuffer[row][column] == '--':
                        return [row, column]
        # all pieces other than pawn; bishop, knight, rook, queen
        else:
            for column in range(2):
                if gamestate.wBuffer[gamestate.bufferMap[piece[1]]][column] == '--':
                    return [gamestate.bufferMap[piece[1]], column]

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
    for i in range(len(gamestate.wBuffer)):
        for p in range(len(gamestate.wBuffer[i])):
            #print(gamestate.wBuffer[i][p])
            if gamestate.wBuffer[i][p] != '--':
                posMap[(15-(i*2))][p*2].state = gamestate.wBuffer[i][p]

    for i in range(len(gamestate.bBuffer)):
        for p in range(len(gamestate.bBuffer[i])):
            #print(gamestate.wBuffer[i][p])
            if gamestate.bBuffer[i][p] != '--':
                posMap[(15-(i*2))][(p*2)+22].state = gamestate.bBuffer[i][p]
    return posMap


# Creates a heuristic map of weights equal to the distance from the destination position
def create_heuristic_map(posMap, endPos):
    for i in range(len(posMap)):
        for j in range(len(posMap[i])):
            if posMap[i][j].state == '. ' and i != 0 and i != len(posMap)-1:
                straightLineDist = math.sqrt(math.pow(endPos[0]-i,2) + math.pow(endPos[1]-j, 2))
                posMap[i][j].heuristic = straightLineDist
            else:
                posMap[i][j].heuristic = math.inf


    posMap[endPos[0]][endPos[1]].isGoal = 1
    return posMap

# Straightline path compression for gantry optimization
def sl_compression(solution):
    compressed_path = []
    compressed_path.append(solution[0])
    for i in range(1,len(solution)-1):
        if solution[i][1] == solution[i+1][1]:
            pass
        else:
            compressed_path.append(solution[i])
    compressed_path.append(solution[len(solution)-1])
    return compressed_path

# Returns the Astar path of
def greedy(heurMap, startNode):
    solution = []
    frontier = []
    explored = set()

    frontier.append((startNode, ''))
    frontierCount = 1
    expandCount = 0

    if startNode.isGoal:
        return solution
    while len(frontier) != 0:
        node = heapq.heappop(frontier)
        solution.append(node)
        if node[0].isGoal:
            return solution

        explored.add(node)
        succ = node[0].successors(heurMap)
        expandCount += 1
        if expandCount >= 100000:
            print("Search halted")
            return -1
        bestNode = (Node(), '')
        for n in succ:
            succNode = n[0]
            if succNode.heuristic != math.inf and n not in explored:
                if bestNode[0].heuristic > succNode.heuristic:
                    bestNode = n
            else:
                pass
            if succNode.isGoal == 1:
                solution.append(n)
                return solution
        frontier.append(bestNode)

    print("no solution")
    # print("path cost: N/A since no solution was found")
    print("frontier: " + str(frontierCount))
    print("expandCount: " + str(expandCount))
    return -1

# Returns an 8-bit address message
def message_encode(value, type):
    justValue = 0b11100000 | int(value)  # Populate hot bits in message type bits
    message = justValue& message_types[type]
    print("\nEncoded", type, "message:", format(message, '#010b'))
    return message



# 328P UART conversation for controlling EM
def transmit_path(path):
    # ADD X (path[0])
    node = path[0][0]
    global currentGantryPos
    currentGantryPos = node.pos
    #print("XADD Message: ",format(message_encode(node.pos[1],"XADDRESS"), '#010b'))
    send_to_328p(message_encode(node.pos[1],"XADDRESS"))
    # ADD Y
    #print("YADD Message: ",format(message_encode(node.pos[0],"YADDRESS"), '#010b'))
    send_to_328p(message_encode(node.pos[0],"YADDRESS"))
    # GO
    #print("GO Message: ",format(message_encode(0b11111,"GO"), '#010b'))
    send_to_328p(message_encode(0b11111,"GO"))
    # Wait for ARRIVED
    #print("Wait for ARRIVED and gantry position (Mocking with sleep for now)")
    resp = recv_from_328p("ARRIVED", 10)
    if resp == -1:
        return -1
    # Request RFID
    #print("RFID Req: ",format(message_encode(0b11010,"RFID"), '#010b'))
    #send_to_328p(message_encode(0b11010,"RFID"))
    # Check RFID, compare to my state
    #print("Recieve and confirm RFID (Mocking with sleep for now)")
    #print("Skip RFID wait for now...")
    #recv_from_328p("RFID", 10)
    # EM ON
    #print("EM Message: ",format(message_encode(0b11111,"EM"), '#010b'))
    send_to_328p(message_encode(0b11111,"EM"))
    #print("Wait for EM ON message (Mocking with sleep for now)")
    recv_from_328p("EM", 10)

    # Loop path[1] and on:
    time.sleep(.5)
    for i in path[1:len(path)]:
        node = i[0]
        currentGantryPos = node.pos
        #print("XADD Message: ", format(message_encode(node.pos[1], "XADDRESS"), '#010b'))
        send_to_328p(message_encode(node.pos[1], "XADDRESS"))
        time.sleep(.03)
        #print("YADD Message: ", format(message_encode(node.pos[0], "YADDRESS"), '#010b'))
        send_to_328p(message_encode(node.pos[0], "YADDRESS"))
        time.sleep(.03)
        #print("GO Message: ", format(message_encode(node.pos[0], "GO"), '#010b'))
        send_to_328p(message_encode(node.pos[0], "GO"))
        #print("Wait for ARRIVED and gantry position (Mocking with sleep for now)")
        recv_from_328p("ARRIVED", 10)
        #time.sleep(1)
    # EM OFF
    #print("EM Message: ",format(message_encode(0b00000,"EM"), '#010b'))
    send_to_328p(message_encode(0b00000,"EM"))
    # Wait for EM OFF?
    recv_from_328p("EM", 10)

    #time.sleep(.5)

    #Add if for topple king

    return


def find_message_type(message):
    for key in message_types:
        if (message&0b11100000) == (message_types[key]&0b11100000):
            return key
    return "Unknown"


# Receive message from 328P via UART
def recv_from_328p(messageType, timeout):
    print("\nWaiting for message:", messageType)

    while True:
        ser.flush()
        #time.sleep(0.03)
        x = ser.read()
        intMessage = int.from_bytes(x, 'little')
        recType = find_message_type(intMessage)
        print(recType, "message recieved", format(intMessage, '#010b'))
        if recType == "BUSY":
            print("Gantry is busy. Waiting for next message")
            #recv_from_328p(messageType)

        if recType != messageType:
            print("WARNING: Recieved message:",recType,"; expected:",messageType)
        if messageType == "RFID":
            print("Do nothing...")
            return
        elif messageType == "ARRIVED":
            xTrue = recv_from_328p("XADDRESS", 10)
            yTrue = recv_from_328p("YADDRESS", 10)
            if xTrue or yTrue == -1:
                print("Exiting, current address is not verified") # This could be where we try to move it back or call a scan
                return 0
            # Verify addresses
            return
        elif messageType == "XADDRESS":
            expectedX_Addr = currentGantryPos[1]
            recX_Addr = (intMessage&0b00011111)
            if expectedX_Addr != recX_Addr:
                print("ERROR: Received x address:",recX_Addr,"expected x address:",expectedX_Addr)
                return
            else:
                print("Confirmed x address ({})".format(recX_Addr))
                return
        elif messageType == "YADDRESS":
            expectedY_Addr = currentGantryPos[0]
            recY_Addr = (intMessage&0b00011111)
            if expectedY_Addr != recY_Addr:
                print("ERROR: Received y address:",recY_Addr,"expected y address:",expectedY_Addr)
                return
            else:
                print("Confirmed y address ({})".format(recY_Addr))
                return
        elif messageType == "EM":
            print("EM confirmed")
            return
        else:
            print("Received unsupported message type:",recType,"expected:",messageType)
            time.sleep(.3)

    return -1 # timeout or error



# Sends 328P a path via UART
def send_to_328p(data):
    ser.flush()
    print("Message sent (" + hex(data)+")","(Header:", (data&0b11100000),"Payload:",(data&0b00011111),')')
    ser.write(data.to_bytes(1, 'little'))  # transmit data serially

    return 0

def print_posMap(map, path=None):
    if (path != None):
        for i in range(len(path)):
            solNode = path[i][0]
            map[solNode.pos[0]][solNode.pos[1]].state = u"\u26AA"
    print("\033[1m\tWhite \t\t\t\t\t\t\tBoard \t\t\t\t\t\tBlack")
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



def make_physical_state_congruent(gs, nextGs):
    posMapA = gamestate_to_position_map(gs)
    posMapB = gamestate_to_position_map(nextGs)
    print_posMap(posMapA)
    print_posMap(posMapB)
    takenFrom = []
    for posB_row in posMapB:
        for posB in posB_row:
            if posB.state != '. ':
                #print(posB.state)
                if posMapA[posB.pos[0]][posB.pos[1]].state == posB.state:   # Already in correct pos
                    #print("Pass")
                    pass
                else:
                    foundReplacement = False
                    for posA_row in posMapA:
                        for posA in posA_row:
                            #print("Checking state, pos", posA.state,posA.pos)
                            if posA.state == posB.state and posA.pos not in takenFrom and posA.state != posMapB[posA.pos[0]][posA.pos[1]].state:
                                #print("posA:", posA.pos)
                                takenFrom.append(posB.pos)
                                #print("Start:", posA.pos)
                                #print("Dest:", posB.pos)
                                make_physical_move(gs, None, startOverride=posA.pos, destOveride=posB.pos)
                                foundReplacement = True
                                break;
                        if foundReplacement:
                            posMapA[posB.pos[0]][posB.pos[1]].state = posB.state
                            posMapA[posA.pos[0]][posA.pos[1]].state = ". "
                            print_posMap(posMapA)
                            break;

    return 0 # Should be congruent

def topple_king(kingCell):
    print("Topple King Called on Gantry")
    kingPos[0] = (int(kingCell[1]) * 2) - 1
    kingPos[1] = letterToColumn[kingCell[0]]
    send_to_328p(message_encode(kingPos[1], "XADDRESS"))
    send_to_328p(message_encode(kingPos[0], "YADDRESS"))
    send_to_328p(message_encode(0b11111, "GO"))
    resp = recv_from_328p("ARRIVED", 10)
    if resp == -1:
        return -1
    send_to_328p(message_encode(0b01010,"EM"))
    return 0

# External function used to interface with GUI and game execution. Takes current gamestate and string move (ie 'e4e5')
def make_physical_move(gamestate, move, startOverride=None, destOveride=None):
    # TODO Extract and interpret move as start and end pos
    posMap = gamestate_to_position_map(gamestate)  # convert 8x8 to position map

    startPos = [0,0]
    endPos = [0, 0]
    if move is not None:
        startPos[0] = (int(move[1]) * 2) - 1
        startPos[1] = letterToColumn[move[0]]

        endPos[0] = (int(move[3:len(move)]) * 2) - 1
        endPos[1] = letterToColumn[move[2]]
    else:
        startPos = startOverride
        endPos = destOveride

    destNode = posMap[endPos[0]][endPos[1]]

    if destNode.state != '. ':
        capturedPos = destNode.pos
        bufferPos = next_buffer_pos(gamestate, destNode.state)
        if destNode.state[0] == 'b':
            bufferPosMap = [(15 - (int(bufferPos[0]) * 2)), (int(bufferPos[1]) * 2) + 22]
        else:
            bufferPosMap = [(15-(int(bufferPos[0])*2)), int(bufferPos[1])*2]
        make_physical_move(gamestate, None, capturedPos, bufferPosMap)

    heurMap = create_heuristic_map(posMap, endPos)

    solution = greedy(heurMap, heurMap[startPos[0]][startPos[1]])
    print("\nBefore Straightline Path Compression: ")
    print_posMap(heurMap, solution)
    resp = transmit_path(sl_compression(solution))

    #if resp == -1:
    #    make_physical_move(gamestate, move, startOverride, destOveride)

    return 0

def transmit_uart_sim():
    while True:
        time.sleep(.03)
        send_to_328p(0x91)
