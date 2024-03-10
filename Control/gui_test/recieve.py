#!/usr/bin/env python3
# -*- coding: utf8 -*-
import tkinter
from tkinter import ttk

from socket import socket, AF_INET, SOCK_STREAM
import threading

HOST = 'localhost'
PORT = 51000
MAX_MESSAGE = 2048
NUM_THREAD = 4

CHR_CAN = '\18'
CHR_EOT = '\04'

cuiroot = tkinter.Tk()

cuiroot.title(u"information panel")
cuiroot.geometry("350x400+100+50")

var1 = tkinter.StringVar()

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

            message('MESSAGE:' + mess)

        except:
            print('Error')

    sock.close()

def message(mes):
    var1.set(mes)

def com_start():
    #別スレッドで待ち受け
    th=threading.Thread(target=com_receive)
    th.start()

frame1 = ttk.Frame(
    cuiroot,
    padding=5)
frame1.grid()

#このラベルに表示
label1 = tkinter.Label(
    frame1,
    anchor="nw",
    width=40,
    height=20,
    foreground="#ff0000",
    background='#000000',
    textvariable=var1)
label1.grid(row=2,column=1)

com_start()
cuiroot.mainloop()