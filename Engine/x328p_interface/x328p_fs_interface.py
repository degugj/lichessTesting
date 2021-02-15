# Module and helper functions for interfacing with fast scanning 328P via I2C
# Authors: Weishan Li, Jack DeGuglielmo
# Date: 2020-11-01
import numpy as np
import time
#import smbus
letterToColumn = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# I2C channel 1 is connected to the GPIO pins
channel = 1
#  MCP4725 defaults to address 0x60
address = 0x60
# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0x40
# Initialize I2C (SMBus)
#bus = smbus.SMBus(channel)


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

def return_message_type(byteMessage):
    # Length check
    # Find type
    print("Received data:", byteMessage, '(' + format(byteMessage, '#010b') + ')')

    return 0

def fast_scan_simulator():
    #https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
    #https://pypi.org/project/smbus2/
    print("-- Fast Scanning Simulation Started --")
    while True:
        with smbus.SMBus(channel) as bus:
            # Read 3 bytes of data via i2c
            recBytes = bus.read_i2c_block_data(address, 0, 3)
            return_message_type(recBytes)
            time.sleep(.3)

            # Write message via i2c
            bus.write_i2c_block_data(address, 0, recBytes)
            print("Transmitting message:", format(recBytes,'#010b'))