#! /usr/bin/env python
import datetime
import csv
import threading
import tkinter
from tkinter import ttk
import pandas as pd

from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.Exceptions import CardConnectionException

NUM_THREAD = 4
cuiroot = tkinter.Tk()

cuiroot.title("information panel")
cuiroot.geometry("1000x800")
disp_text = tkinter.StringVar()

buttons = {}

gui_com = 0 #ボタンの入力を受け取る変数
gui_event = 0 #guiのページの指定 0:"タグをかざしてください" 1:"取り出すものを選択してください"[在庫分のボタンを表示] 2:"取り出し中"[ボタンを消す] 3:"取り出してください" 4:"格納セル待ち" 5:返却してください 6:"ボックスがいっぱいです"

def gui_main():
    if gui_event == 0:
        disp_text.set("タグをかざしてください")
        button_disappear()
    elif gui_event == 1:
        disp_text.set("取り出すものを選択してください")
        button_appear()
    elif gui_event == 2:
        disp_text.set("取り出し中")
    elif gui_event == 3:
        disp_text.set("取り出してください")
    elif gui_event == 4:
        disp_text.set("格納セル待ち")
    elif gui_event == 5:
        disp_text.set("返却してください")
    elif gui_event == 6:
        disp_text.set("ボックスがいっぱいです")

    cuiroot.mainloop() 

def button_appear():
    #state.csvの情報を読む
    df = pd.read_csv('state.csv',header=None)
    df = df[df.iloc[:, 1] != -1]
    print(df)

    # 読み込んだ情報をもとに取り出し用のボタンを作成
    for index, row in df.iterrows():
        button = create_button(str(row.iloc[1]),str(row.iloc[2]))
        button.place(x=10 + index * 150, y=300)  # ボタンの位置を調整
        buttons[str(row.iloc[2])] = button


def button_disappear():
    # 既存のボタンを全て削除
    for button in buttons.values():
        button.destroy()
    buttons.clear()                     

def gui_start():
    #別スレッドで待ち受け
    thread_gui = threading.Thread(target=gui_main)
    thread_gui.start()

def button_num(num):
    gui_com = num

def create_button(num,text):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(cuiroot, text=text,height=3, width=7, font=Font,command=lambda: button_num(num))
    buttons[text] = button
    return button

#このラベルに表示
label1 = tkinter.Label(
    cuiroot,
    anchor="nw",
    width=100,
    height=8,
    foreground="#000000",
    background='#87cefa',
    textvariable=disp_text,
    font=("MSゴシック", 20))
label1.place(x=10,y=10)


def base_sys():
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

    print("タグをタッチしてください")

    flag = True

    while True:
        gui_com = 0
    
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

                    #guiのボタンを発生させる
                    gui_event = 1 #1:"取り出すものを選択してください"[在庫分のボタンを表示]
                    #guiの入力があるまで待つ
                    while True:
                        if gui_com != 0:
                            break   

                    input_number = gui_com #input("数値を入力してください: ")
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
                    gui_event = 2 #2:"取り出し中"[ボタンを消す]
                    #モーターを動かす（取り出し）
                    '''
                    while True:
                        if gui_com != 0:
                            break
                    '''                
                else:
                    #シリアルIDカードをかざした場合
                    ##格納動作
                    gui_event = 4 #4:"格納セル待ち"
                    for i in range(len(cell_ID)):
                        if serial_ID[i] == "-1" :
                            serial_ID[i] = string
                            print("cell_ID: ",cell_ID[i],"に格納します")    
                            for row in manage_data:
                                if row[0] == string:
                                    row[4] = username
                                    row[3] = machine_ID
                            ## ここに格納処理
                            #モータを動かす
                            '''
                            while True:
                                if gui_com != 0:
                                    break
                            '''
                                    
                            gui_event = 5 #5:返却してください
                            '''
                            while True:
                                if gui_com != 0:
                                    break
                            '''
                            break               
                    else:
                        gui_event = 6 #6:"ボックスがいっぱいです"
                        '''
                        while True:
                            if gui_com != 0:
                                break
                        '''    
                        print("ボックスがいっぱいです")

                gui_com = 0
                gui_event = 0 #0:"タグをかざしてください"

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
                #print("Not found1")
                flag = True
                print("タグをタッチしてください")
        
        except CardConnectionException:
            if flag == False:
                #print("Not found2")
                flag = True
                print("タグをタッチしてください")
       
        except IndexError:
            if flag == False:
                #print("Read Error")
                flag = True

thread_base = threading.Thread(target=base_sys)
gui_start()
thread_base.start()


