#! /usr/bin/env python

from smartcard.System import readers

# define the APDUs used in this script
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0xA0, 0x00, 0x00, 0x00, 0x62,
    0x03, 0x01, 0x0C, 0x06, 0x01]
COMMAND = [0x00, 0x00, 0x00, 0x00]

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]# get UID command

GET_INF_00 = [0xFF, 0xB0 ,0x00, 0x06, 0x00]
GET_INF_01 = [0xFF, 0xB0 ,0x00, 0x04, 0x00]
# get all the available readers
r = readers()
#print("Available readers:", r)

reader = r[0]
#print("Using:", reader)

connection = reader.createConnection()
connection.connect()


data_01, sw1_01, sw2_01 = connection.transmit(GET_INF_01)
data, sw1, sw2 = connection.transmit(GET_INF_00)

#data, sw1, sw2 = connection.transmit(SELECT)
#data, sw1, sw2 = connection.transmit(GET_UID)
data_size = data_01[1] - 6
extracted_bytes = data[1:data_size]
ascii_chars = [chr(byte) for byte in extracted_bytes]
string = ''.join(ascii_chars)
print(string)

#print(data)
#print(data_01)
print("Select Applet: %02X %02X" % (sw1, sw2))

#data, sw1, sw2 = connection.transmit(COMMAND)
#print(data)
#print("Command: %02X %02X" % (sw1, sw2))