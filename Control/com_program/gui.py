###!/usr/bin/env python3
# -*- coding: utf8 -*-
import tkinter
from tkinter import ttk
import pandas as pd

from socket import socket, AF_INET, SOCK_STREAM
import threading

HOST = 'localhost'
PORT = 51000
MAX_MESSAGE = 2048
NUM_THREAD = 4

CHR_CAN = '\18'
CHR_EOT = '\04'

cuiroot = tkinter.Tk()

cuiroot.title("information panel")
cuiroot.geometry("1000x800")

var1 = tkinter.StringVar()

buttons = {}

def com_receive():
    #global sock
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind ((HOST, PORT))
    sock.listen (NUM_THREAD)
    print ('receiver ready, NUM_THREAD = ' + str(NUM_THREAD))
    while True:
        try:
            conn,addr = sock.accept()
            mess = conn.recv(MAX_MESSAGE).decode('utf-8')

            conn.close()
            if(mess == CHR_EOT):
                break
            
            if(mess == CHR_CAN):
                continue

            if(mess == 'tool_extract'):
                print("index")
                df = pd.read_csv('state.csv',header=None)
                df = df[df.iloc[:, 1] != -1]
                print(df)
                '''
                # 既存のボタンを全て削除
                for button in buttons.values():
                    button.destroy()
                buttons.clear()
                '''
                # ボタンを作成
                for index, row in df.iterrows():
                    button = create_button(str(row.iloc[1]),str(row.iloc[2]))
                    button.place(x=10 + index * 150, y=300)  # ボタンの位置を調整
                    buttons[str(row.iloc[2])] = button
            '''
            if(mess != 'tool_extract'):
                message('Retrieving work in progress')
            '''
            # 既存のボタンを全て削除
            for button in buttons.values():
                button.destroy()
            buttons.clear()
            
            if(mess == 'box_full'):
                
                message('Box is full')

            if(mess == 'stand'):
                message('Please touch the tag')
            
            if(mess == 'return'):
                message('Setting storage location...')

        except:
            print('Error')
    sock.close()

def message(mes):
    var1.set(mes)

def com_start():
    #別スレッドで待ち受け
    th=threading.Thread(target=com_receive)
    th.start()

def send_button_text(text):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(text.encode('utf-8'))
    sock.close()

def create_button(num,text):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(cuiroot, text=text,height=3, width=7, font=Font,command=lambda: send_button_text(num))
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
    textvariable=var1,
    font=("MSゴシック", 20))

label1.place(x=10,y=10)

com_start()
cuiroot.mainloop()