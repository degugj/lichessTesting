# i2ctest.py
# Used sparkfun website to learn RaspPi I2C
# https://www.sparkfun.com/products/8736
#modified for i2c demo

import smbus
import time

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  Address of MCP2300-8
address = 0x27

# GPIO Register on MCP2300-8
# Controls Output on GPIO Pins
reg_GPIO = 0x09


# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)


#configure output
reg_IODIR = 0x00 #IO Direction Register Addr
IODIR_Val = 0x00 #Set all pins to output

# Write IODIR_Val to IODIR Register
bus.write_byte_data(address, reg_IODIR, IODIR_Val)

#Initial Declare of msg
msg = 0x00

i = 1
while (i > 0):


	# Write msg to reg_GPIO to configure output
	bus.write_byte_data(address, reg_GPIO, msg)
	msg = msg+1
#	time.sleep(.3)
