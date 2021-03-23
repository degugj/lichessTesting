# Module and helper functions for interfacing with fast scanning 328P via I2C
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01
import numpy as np
import time
#import serial
#ser2 = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
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
        self.chessCell = None

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
        #print("fs_column:",fs_column)
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

        # print(bin(column_to_byte(column)))
        # print(bin(messageArray[c].data))

def compare_chess_states(gs, messageArray):
    #print("GS: ", gs)
    #print("Sam's Message Array:", messageArray)
    for i in range(8):
        column = get_column_byIndex(gs, i)
        #print(column)
        #print(column_to_byte(column))
        if(column_to_byte(column) != messageArray[i].data):
            print("Incongruent gamestates")
            return -1
    print("Verified Congruent Gamestates")
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
    # Step 1: Tell Sam to transmit all columns
    # Step 2: Sam transmits current state (column by column).
    # Wait for 8 messages. Compare array to gs.
    # return to wei 1, -1, 0
    return 0

def receive_chess_state():
    samState = []
    while True:
        # Serial receive 2 bytes from Sam
        # ser.flush()
        # rawRecByte0 = ser.read()
        # Maybe add a delay here
        # rawRecByte1 = ser.read()
        # recByte0 = int.from_bytes(rawRecByte0, 'little')
        # recByte1 = int.from_bytes(rawRecByte1, 'little')
        #recByte0 = 0b11110010
        recByte1 = 0b11000011
        #messageType = (recByte0 >> 3)
        messageType = None
        #messageCol = recByte0 & 0b00000111
        messageCol = None
        currentMessage = gamestateMessage(messageType, messageCol, recByte1)

        # Figure out message type
        # messageTypeStr = message_types[messageType]

        samState.append(currentMessage)

        if(len(samState) == 8):
            return samState

    return -1

def start_fast_scan(gs):
    newGs = np.array(gs.board)

    # Serial write start message to Sam
    transmission_byte0 = 0b00100111
    transmission_byte1 = 0b00100111  # Second byte doesn't matter for start

    # After transmission. Sam will send all 8 columns to check if we have congruent states
    samInitialState = receive_chess_state()
    if samInitialState == -1:
        print("Error in reading Sam State")
        return -1
    # Check congruency
    if(compare_chess_states(newGs, samInitialState) != 0):
        print("Incongruent Gamestates. Returning 5 to Wei to tell user to fix pieces and call start again")
        return 5

    # Transmit again
    samState2 = receive_chess_state()
    if(samState2 != -1):
        # Finesse for testing the move resolution
        samState2[7].data = 0b11000101
        move = resolve_chess_move(newGs, samState2)
        if move == '':
            # add a length check if we only get one cell resolved
            print("No move detected/resolved")
            return -1
        return move
    else:
        print("Error resolving move/start FS function")
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
""""
def test_sim():
     numb = 1
     print ("Enter 1 for ON or 0 for OFF")
     while numb == 1:
        ledstate = input(">>>>   ")
        if ledstate == "1":
             #bus.write_byte(address, 0x1) # switch it on
        elif ledstate == "0":
             #bus.write_byte(address, 0x0) # switch it on
        else:
             numb = 0
"""
