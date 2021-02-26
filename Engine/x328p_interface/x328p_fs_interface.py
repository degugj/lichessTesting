# Module and helper functions for interfacing with fast scanning 328P via I2C
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01
import numpy as np
import time
from smbus import SMBus
letterToColumn = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
message_types = {'NA':0b00000111, 'Piece Picked Up':0b00001111, 'Piece Put Down':0b00010111, 'Invalid I2C Command':0b01011111}
# I2C channel 1 is connected to the GPIO pins
channel = 1
#  MCP4725 defaults to address 0x60
address = 0x8
# Register addresses (with "normal mode" power-down bits)
#reg_write_dac = 0x40
# Initialize I2C (SMBus)
bus = SMBus(channel)


def get_column(gsNP, columnChar):
    return gsNP[:,letterToColumn[columnChar]]

def column_to_byte(column):
    columnByte = '0'
    print(format(columnByte, '#010b'))
    return 0

def start_fast_scan(gs):
    newGs = np.array(gs.board)
    return 0

def stop_fast_scan():
    return 0

def print_message_info(two_byte_message):
    return 0

def return_message_type(byteMessage):
    # Length check
    # Find type
    #print("Received data:", byteMessage, '(' + format(byteMessage, '#010b') + ')')
    byte1 = byteMessage[0]
    for key in message_types:
        if (byte1&0b11111000) == (message_types[key]&0b11111000):
            return key
    return 'Unknown'

def fast_scan_simulator():
    #https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
    #https://pypi.org/project/smbus2/
    print("-- Fast Scanning Simulation Started --")
    while True:
            # Read 3 bytes of data via i2c
            startMessageB1 = 0x30
            startMessageB2 = 0xFF
            #startMessage = [startMessageB1, startMessageB2]
            bus.write_byte(address, startMessageB1)
            #bus.write_byte(address, startMessageB2)
            print("Transmitting Bytes:",startMessageB1)
            #time.sleep(.3)
            recBytes = bus.read_i2c_block_data(address, 0, 2)
            #return_message_type(recBytes)
            print("Received Message Type:"+return_message_type(recBytes))
            print("Recveived Bytes:", recBytes)
            time.sleep(5)

            # Write message via i2c
            #bus.write_i2c_block_data(address, 0, recBytes)
            #print("Transmitting message:", format(recBytes,'#010b'))
def test_sim():
     numb = 1
     print ("Enter 1 for ON or 0 for OFF")
     while numb == 1:
        ledstate = input(">>>>   ")
        if ledstate == "1":
             bus.write_byte(address, 0x1) # switch it on
        elif ledstate == "0":
             bus.write_byte(address, 0x0) # switch it on
        else:
             numb = 0
