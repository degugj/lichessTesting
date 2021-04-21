# Module and helper functions for interfacing with fast scanning 328P via I2C Authors: Weishan Li, Jack DeGuglielmo Date: 2020-11-01
import numpy as np
from datetime import datetime
import time
import serial
import spidev
spi = spidev.SpiDev()
bus = 0
device = 0
spi.open(bus, device)

# Settings (for example)
spi.max_speed_hz = 5000
spi.mode = 0b00

ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
letterToColumn = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,'g': 6,'h': 7}  # To translate cell to posMap location
columnToLetter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
message_types = {0b00000 : 'N/A', 0b00001: 'Piece Picked Up', 0b00010: 'Piece Put Down', 0b01011: 'Invalid I2C Command'}
# I2C channel 1 is connected to the GPIO pins
channel = 1
#  MCP4725 defaults to address 0x60
address = 0x03
# Register addresses (with "normal mode" power-down bits)
#reg_write_dac = 0x40
# Initialize I2C (SMBus)
#bus = SMBus(channel)
import math

class gamestateMessage():
    def __init__(self, typ, col, data):
        self.typ = typ
        self.col = col
        self.data = data
        self.timestamp = None
        self.chessCell = None

    def __str__(self):
        time = self.timestamp.strftime("%H:%M:%S")
        line1 = "Fast Scan Message ID: " + str(id(self)) + " at time:" + time
        line2 = "- Type: "+ format(self.typ, '#010b') + " | Column: " + str(self.col) +" (" + columnToLetter[self.col] + ") | Data: " + format(self.data, "#010b")+ " -\n"
        return (line1+'\n'+line2)

    def equals(self, nextMessage):
        if self.typ == nextMessage.typ and self.data == nextMessage.data and self.col == nextMessage.col:
            return True
        return False

    # return chess cell indicated by col integer
    """
    def return_chess_cell(self):
        #print("Column: ", columnToLetter[self.col])
        charColumn = columnToLetter[self.col]
        #print(bin(self.data))
        if self.data != 0:
            print("Get row from data: ", int(math.log(self.data,2)+1))
            chessRow = int(math.log(self.data,2)+1)
        cell = columnToLetter[self.col] + str(chessRow)
        print("Cell:",cell)
        return cell
    """
def resolve_chess_move(gs, messageArray):
    #print("Resolving Move...")
    #print("GS: ", gs)
    #print("Sam's Message Array:", messageArray)
    start_found = False
    dest_found = False

    start_pos = ""
    dest_pos = ""

    # loop through each column
    for c in range(len(gs)):
        # convert column to byte form to compare with fast scan byte (i.e 0b11000011)
        column = column_to_byte(get_column_byIndex(gs, c))
        #print("column:",column)
        fs_column = messageArray[c].data
        #print("fs_column:",bin(fs_column))
        # loop through each cell of column
        for i in range(len(gs)):
            # bit shift to find value of current cell
            cell = (column >> i) & 1
            cell_fs = (fs_column >> i) & 1

            # check for start location; once found, turn bool off
            if cell_fs == 0 and cell == 1 and not start_found: 
                start_cell_letter = columnToLetter[c]    
                start_cell_number = i+1

                # convert to chess coordinates and concatenate (i.e a2)
                start_pos = start_cell_letter + str(start_cell_number)
                start_found = True
            
            # check for destination location; once found, turn bool off
            if cell_fs == 1 and cell == 0 and not dest_found:
                dest_cell_letter = columnToLetter[c]
                dest_cell_number = i+1

                # convert to chess coordinates and concatenate (i.e b4)
                dest_pos = dest_cell_letter + str(dest_cell_number)
                dest_found = True
    return start_pos + dest_pos


def find_start_cell(gs, messageArray):
    start_pos = ""

    # loop through each column
    for c in range(len(gs)):
        # convert column to byte form to compare with fast scan byte (i.e 0b11000011)
        column = column_to_byte(get_column_byIndex(gs, c))
        # print("init column:", bin(column))
        # print("column:",column)
        fs_column = messageArray[c].data
        # print("fs_column:",bin(fs_column))
        # loop through each cell of column
        for i in range(len(gs)):
            # bit shift to find value of current cell
            # print("Evaluating:", gs[7-i][c])
            cell = (column >> i) & 1
            cell_fs = (fs_column >> i) & 1

            # check for start location; once found, turn bool off
            if cell_fs == 0 and cell == 1:
                start_cell_letter = columnToLetter[c]
                start_cell_number = i + 1

                # convert to chess coordinates and concatenate (i.e a2)
                start_pos = start_cell_letter + str(start_cell_number)
                # print("Column before:", gs[c-1])
                # print("Column after:", gs[c + 1])
                # print("GS[c]:",gs[c])
                # print("cell at:",gs[c+1][7-i])
                # print("cell before:", gs[c+1][6 - i])
                # print("cell after:", gs[c+1][8 - i])

                return [start_pos, gs[7-i][c]]

    return -1

def resolve_chess_move_v2(gs, statePrev, stateNext):
    # print("Resolving Move...")
    # print("GS: ", gs)
    # print("Sam's Message Array:", messageArray)
    if compare_message_lists(statePrev, stateNext):
        print("Same state transmitted")
        return 1

    cell = ""

    # loop through each column
    for c in range(8):
        fs_columnPrev = statePrev[c].data
        fs_columnNext = stateNext[c].data
        # print("fs_column:",bin(fs_column))
        # loop through each cell of column
        for i in range(8):
            # bit shift to find value of current cell
            cellBitPrev = (fs_columnPrev >> i) & 1
            cellBitNext = (fs_columnNext >> i) & 1

            # check for start location; once found, turn bool off
            if cellBitPrev == 0 and cellBitNext == 1:
                start_cell_letter = columnToLetter[c]
                start_cell_number = i + 1

                # convert to chess coordinates and concatenate (i.e a2)
                cell = start_cell_letter + str(start_cell_number)
                return [cell, gs[c][7-i]]

            elif cellBitPrev == 1 and cellBitNext == 0:
                start_cell_letter = columnToLetter[c]
                start_cell_number = i + 1

                # convert to chess coordinates and concatenate (i.e a2)
                cell = start_cell_letter + str(start_cell_number)
                return [cell, gs[c][7-i]]
    return -1

def resolve_chess_move_v3(gs, statePrev, stateNext):
    # print("Resolving Move...")
    # print("GS: ", gs)
    # print("Sam's Message Array:", messageArray)
    if compare_message_lists(statePrev, stateNext):
        print("Same state transmitted")
        return 1

    cell = ""

    # loop through each column
    for c in range(8):
        fs_columnPrev = statePrev[c].data
        fs_columnNext = stateNext[c].data
        # print("fs_column:",bin(fs_column))
        # loop through each cell of column
        for i in range(8):
            # bit shift to find value of current cell
            cellBitPrev = (fs_columnPrev >> i) & 1
            cellBitNext = (fs_columnNext >> i) & 1

            # check for start location; once found, turn bool off
            if cellBitPrev == 0 and cellBitNext == 1:
                start_cell_letter = columnToLetter[c]
                start_cell_number = i + 1

                # convert to chess coordinates and concatenate (i.e a2)
                cell = start_cell_letter + str(start_cell_number)
                #print(gs[7-i])
                return [cell, gs[7-i][c]]

            elif cellBitPrev == 1 and cellBitNext == 0:
                start_cell_letter = columnToLetter[c]
                start_cell_number = i + 1

                # convert to chess coordinates and concatenate (i.e a2)
                cell = start_cell_letter + str(start_cell_number)
                return [cell, gs[7-i][c]]
    return -1



def compare_message_lists(stateA, stateB):
    for i in range(8):
        if not stateA[i].equals(stateB[i]):
            return False
    return True

def compare_chess_states(gs, messageArray):
    #print("GS: ", gs)
    #print("Sam's Message Array:", messageArray)
    for message in messageArray:
        column = get_column_byIndex(gs, message.col)
        #print(column)
        #print(column_to_byte(column))
        if(column_to_byte(column) != messageArray[message.col].data):
            return -1
    #print("Verified Congruent Gamestates")
    return 0

def return_message_dict(two_byte_message):
    # Talked to Wei about this
    dict = {}
    return dict

def get_column_byChar(gsNP, columnChar):
    return gsNP[:,letterToColumn[columnChar]]

def get_column_byIndex(gsNP, ind):
    return gsNP[:,ind]

def column_to_byte(column):
    columnInt = 0b00000000
    for piece in column:
        #print(piece)
        if piece != '--':
            columnInt = columnInt << 1
            columnInt = columnInt | 1
        else:
            columnInt = columnInt << 1
            columnInt = columnInt | 0b00000000
    #print(bin(columnInt))
    return columnInt

def initial_error_check(gs):
    newGs = np.array(gs.board)
    print("Starting initial check...")
    #send_to_328p(0b00101000,"Initial Check Data")
    samInitialState = receive_chess_state()
    if samInitialState == -1:
        print("Error in reading Sam State")
        return [-1, None]
    # Check congruency
    if (compare_chess_states(newGs, samInitialState) != 0):
        print("Incongruent Gamestates. Correct physical state and retry")
        return [5, ['a2']]
    print("Initial Gamestates Verified and Congruent")
    return [0, None]

# Receive message from 328P via UART
"""
def recv_from_328p(timeout):
    print("\nWaiting for message:")
    while True:
        ser.flush()
        # time.sleep(0.03)
        x = ser.read()
"""

def receive_chess_state():
    # print("Waiting for Sam's Chess State...")
    samState = []
    send_to_328p(0b00110000, "Start FS Message Sent")
    dumpByte = spi.readbytes(1)
    print("Dup byte:",bin(int.from_bytes(dumpByte,'little')),str(int.from_bytes(dumpByte, 'little')))
    for i in range(8):
        # Serial receive 2 bytes from Sam
        # ser.flush()
        # rawRecByte0 = ser.read()
        send_to_328p(i, "Requesting Column "+ str(i))
        rawRecByte0 = spi.readbytes(1)
        #time.sleep(0.003)
        # Maybe add a delay here
        # rawRecByte1 = ser.read()

        #rawRecByte1 = ser.readbytes(1)
        now = datetime.now()
        #recByte0 = int.from_bytes(rawRecByte0, 'little')
        # print("Byte 0 Received:", format(recByte0, '#010b'))
        recByte0Mirror = int.from_bytes(rawRecByte0, 'little')
        recByte0 = int('{:08b}'.format(recByte0Mirror)[::-1], 2)
        # print("Byte 1 Received:", format(recByte1, '#010b'))
        # recByte0 = 0b11110010
        # recByte1 = 0b11000011
        #messageType = (recByte0 >> 3)
        messageType = 0
        #messageCol = recByte0 & 0b00000111
        messageCol = i
        currentMessage = gamestateMessage(messageType, messageCol, recByte0)
        currentMessage.timestamp = now
        #time.sleep(0.03)
        print(currentMessage)
        # Figure out message type
        # messageTypeStr = message_types[messageType]

        samState.append(currentMessage)
    return samState

# Sends 328P a path via UART
def send_to_328p(data, messageType):
    ser.flush()
    #print(messageType, "message sent (" + hex(data)+")", format(data,'#010b'))
    #while True:
    #    received_data = ser.read()  # read serial port
    #    time.sleep(0.03)
    #    data_left = ser.inWaiting()  # check for remaining byte
    #    received_data += ser.read(data_left)
    #    print("Sent Data: ",format(data, '#010b'))  # print received data
    #ser.write(data.to_bytes(1, 'little'))  # transmit data serially
    spi.writebytes([data])

def start_fast_scan(gs):
    newGs = np.array(gs.board)
    #print("newGs",newGs)
    # Serial write start message to Sam
    #transmission_byte0 = 0b00100111
    #transmission_byte1 = 0b00110111  # Second byte doesn't matter for start
    #send_to_328p(transmission_byte0, "Dump All Sensor Data")
    # Transmit again

    isMoveNotFound = True
    samState = None
    prevSamState = None
    startCell = None
    destCell = None
    isOpponentRemoved = False
    isChangeMade = False
    while isMoveNotFound:
        while isChangeMade == False:
            send_to_328p(0b00110000, 'Prompt Gamestate Status Message')
            stateAnswer = spi.readbytes(1)
            if int.from_bytes(stateAnswer, 'little') == 0xAF:
                isChangeMade == True
        # First one is compared to local gs
        samState = receive_chess_state()
        #print("startCell before entering if", startCell)
        if startCell is None or startCell == -1:  # Check this OR condition
            if not isOpponentRemoved:
                startCell = find_start_cell(newGs, samState)
            else:
                startCell = resolve_chess_move_v3(newGs, prevSamState, samState)
            if startCell != -1 and startCell[1][0] != gs.userColor:
                print("User has lifted opponent's piece. Start Cell has not been resolved.", startCell)
                #newGs[5][4] = '--'
                #samState2 = receive_chess_state()
                startCell = -1
                isOpponentRemoved = True
            else:
                print("Start Cell Resolved:",startCell)
        else:
            # Finesse for testing the move resolution
            # samState2[7].data = 0b11000101
            destCell = resolve_chess_move_v3(newGs, samState, prevSamState)
            # unsure about a check here
            print("Dest Cell Resolved:", destCell)
            if destCell != -1:
                if destCell[0] == startCell[0]: # User changed move
                    print("User placed piece back. Continue making move.")
                    startCell = -1
                    destCell = -1

                if destCell[0] != startCell[0]:
                    # Transmit Stop
                    if destCell[1][0] == gs.get_opponentcolor()[0] and not isOpponentRemoved: 
                         destCell = -1
                         isOpponentRemoved = True
                    else:
                         isMoveNotFound = True
                         print("Destination Cell Resolved:", destCell)
                         # Serial write stop message to Sam
                         transmission_byte0 = 0b00111000
                         send_to_328p(transmission_byte0, "Stop Fast Scan")
                         print("Stop FS sent")
                         return startCell[0] + destCell[0]
                         #print(startCell[0] + destCell[0])


        prevSamState = samState.copy()
    return -1


    #move = resolve_chess_move(newGs, samState)
    #print("Resolved Move:", move)


    # Step 1: Transmit start message to sam

    # Sam waits for completion of move (aka piece placed down or button)
    # Step 2: Sam transmits current state (column by column).
    # Wait for 8 messages. Store in array

    # Step 3: Loop through objects. Resolve physical user move.
    # Should make function to compare 8 messages to current (use for error checking later)



    # Jack generates message from Sam
    #print(get_column(newGs, 'a'))

    # return move
    return 0


def stop_fast_scan():
    return 0

def print_message_info(two_byte_message):
    return 0

def return_message_type(typeInt):
    #print("Received data:", byteMessage, '(' + format(byteMessage, '#010b') + ')')
    return 'Unknown'


def fast_scan_simulator_uart():

    print("-- Fast Scanning Simulation Started --")
    while True:

        print("Waiting for first transmitted byte...")
        #recByte = bus.read_byte(address)
        # = int.from_bytes(x, 'little')

        #print("Recveived Byte:", recByte, '(' + format(integerRecByte, '#010b') + ')')
        time.sleep(.03)


def fast_scan_simulator():
    #https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
    #https://pypi.org/project/smbus2/
    print("-- Fast Scanning Simulation Started --")
    while True:
            # Read 3 bytes of data via i2c
            #startMessageB1 = 0x30
            #startMessageB2 = 0xFF
            #startMessage = [startMessageB1, startMessageB2]
            #bus.write_byte(address, startMessageB1)
            #bus.write_byte(address, startMessageB2)
            #print("Transmitting Bytes:",startMessageB1)
            #time.sleep(.3)
            print("Waiting for first transmitted byte...")
            recByte = bus.read_byte(address)
            integerRecByte = int.from_bytes(x, 'little')
            
            #recBytes = bus.read_i2c_block_data(address, 0, 2)
            #return_message_type(recBytes)
            #print("Received Message Type:"+return_message_type(recBytes))
            print("Recveived Byte:", recByte, '(' + format(integerRecByte, '#010b') + ')')
            time.sleep(.03)

            # Write message via i2c
            #bus.write_i2c_block_data(address, 0, recBytes)
            #print("Transmitting message:", format(recBytes,'#010b'))


def test_sim():
     print("Starting SPI simulation")
     while True:
         time.sleep(2)
         print("Transmitting 0xEA over SPI")
         spi.writebytes([0xEA])
         for i in range(5):
              print("Waiting for transmission from 328...")
              recData = spi.readbytes(1)
              integerRecData = int.from_bytes(recData, 'little')
              print("Received SPI data", hex(integerRecData), bin(integerRecData))
