import stss_gui
import tkinter

func_mode_debug = 0
NFC_arg_debug = 0

def main_menu():
    global current_page
    #実装
    #
    #
    #   wait NFC scanning
    #func_mode = function_number
    func_mode = func_mode_debug
    #arg = argument
    arg = NFC_arg_debug

    current_page = func_mode
    stss_gui.main_function[func_mode](arg)

stss_gui.main_function.append(('main_menu',main_menu))

def deposit(USER_NAME):
    stss_gui.Draw_Page()
    stss_gui.Arrange_ToolButton()

stss_gui.main_function.append(('deposit',deposit))

def withdraw(SERIAL_NUMBER):
    #実装
    #
    #
    pass

stss_gui.main_function.append(('withdraw',withdraw))
    

#print(main_function[0][1])
root = tkinter.Tk()

#
#
#

root.after(3000,main_menu)
root.mainloop()