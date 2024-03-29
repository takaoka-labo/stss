#! /usr/bin/env python
import datetime
import csv
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.Exceptions import CardConnectionException




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


flag = True
while True:
    #time.sleep(2)
   
    try: # Attempt to connect to the card
        connection = reader.createConnection()
        connection.connect()

        data_01, sw1_01, sw2_01 = connection.transmit(GET_INF_01)
        data, sw1, sw2 = connection.transmit(GET_INF_00)

        data_size = data_01[1] - 6
        
        if flag == True:
            flag = False
            extracted_bytes = data[1:data_size]
            ascii_chars = [chr(byte) for byte in extracted_bytes]
            string = ''.join(ascii_chars)
            print(string)

            print("Select Applet: %02X %02X" % (sw1, sw2))
            
            current_time = datetime.datetime.now()
            
            with open('output.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([string, current_time])


    except NoCardException:
        # If no card is found, print a message and continue the loop
        if flag == False:
            print("Not found")
            flag = True
        
    except CardConnectionException:
        if flag == False:
            print("Not found")
            flag = True
        
    except IndexError:
        if flag == False:
            print("Read Error")
            flag = True



#print("Using:", reader)
'''
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
'''