#! /usr/bin/env python
import datetime
import csv
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.Exceptions import CardConnectionException

box_cell_num = 6
machine_ID = 1

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
    
    cell_ID   = []
    serial_ID = []
    tool_name = []
    tool_size = []
    
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
            first_five_chars = string[:5]
            username = string[5:]
            
            
            with open('state.csv', 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    #print(row[0],row[1],row[3])
                    cell_ID.append(row[0])
                    serial_ID.append(row[1])
                    tool_name.append(row[2])
                    tool_size.append(row[3])              
            
            with open('manage.csv', 'r') as f:
                csv_reader = csv.reader(f)
                manage_data = list(csv_reader)
                        
                            
            if first_five_chars == "user.":
               
                 ##取り出し動作
                print("何番の工具を取り出しますか？")
                input_number = input("数値を入力してください: ")
                for i in range(len(serial_ID)):
                    if serial_ID[i] == input_number:  
                        serial_ID[i] = -1
                        tool_name[i] = "none"
                        tool_size[i] = "none"
                        for row in manage_data:
                            if row[0] == input_number:
                                row[4] = username
                                row[3] = "using" 
                        
                    
                ## ここに取り出し処理
                
            else:
                ##格納動作
                for i in range(len(cell_ID)):
                    if serial_ID[i] == "-1" :
                        serial_ID[i] = string
                        print("cell_ID: ",cell_ID[i],"に格納します")    
                        for row in manage_data:
                            if row[0] == string:
                                row[4] = username
                                row[3] = machine_ID
                        ## ここに格納処理
                        break               
                else:
                    print("ボックスがいっぱいです") 
                        
            ##manage.csvから情報を取得してstate.csvの工具情報を更新    
                
            for i in range(len(serial_ID)) :
                for row in manage_data :
                    if serial_ID[i] == row[0]:
                        tool_name[i] = row[1]
                        tool_size[i] = row[2]
                                          
            ##state.csvの情報を最新状態にする
            with open('state.csv', 'w', newline='') as f:
                csv_writer = csv.writer(f)
                for i in range(len(cell_ID)) :
                    print([cell_ID[i], serial_ID[i], tool_name[i], tool_size[i]])
                    csv_writer.writerow([cell_ID[i], serial_ID[i], tool_name[i], tool_size[i]])
            
            ##manage.csvの情報を最新状態にする  
            with open('manage.csv', 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(manage_data)
             #print("Select Applet: %02X %02X" % (sw1, sw2))
            
            current_time = datetime.datetime.now()
            
            with open('log.csv', 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([string, current_time,])
                
    except NoCardException:
        # If no card is found, print a message and continue the loop
        if flag == False:
            print("Not found1")
            flag = True
        
    except CardConnectionException:
        if flag == False:
            print("Not found2")
            flag = True
       
    except IndexError:
        if flag == False:
            print("Read Error")
            flag = True

