#! /usr/bin/env python
import datetime
import csv
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.Exceptions import CardConnectionException

box_cell_num = 6



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

cell_ID   = []
serial_ID = []
tool_name = []
cell_size = []


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
            
            with open('state.csv', 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    cell_ID.append(row[0])
                    serial_ID.append(row[1])
                    cell_size.append(row[3])
            
            with open('manage.csv', 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    for temp in serial_ID:
                        if serial_ID == temp:
                            tool_name.append(row[1])
            
            with open('state.csv', 'w', newline='') as f:
                csv_writer = csv.writer(f)
                for i in range(len(cell_ID)):
                    csv_writer.writerow([cell_ID[i], serial_ID[i], tool_name[i], cell_size[i]])

            
            print("Select Applet: %02X %02X" % (sw1, sw2))
            
   
            current_time = datetime.datetime.now()
            
            with open('log.csv', 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([string, current_time,])
                
                
            
                


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

