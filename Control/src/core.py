from stss_nfc.stss_nfc import *
import stss_gui
import tkinter

func_mode_debug = 1
NFC_arg_debug = 'nishiyama'

#main function : 0
def main_menu(root):
    global current_page
    if stss_gui.after_id != None:
        root.after_cancel(stss_gui.after_id)

    nfc_detected = nfc.connect()
    #func_mode = function_number
    if nfc_detected:
        
        NFC_TYPE,string = nfc.get_data()
        #degugging
        #func_mode = int(input('enter function_number'))
        func_mode = NFC_TYPE
        #arg = NFC_arg_debug
        arg = string
        current_page = func_mode
        stss_gui.main_function[func_mode][1](root,0,arg) # start each function from phase : 0
    else:
        stss_gui.after_id = root.after(100,main_menu,root)

stss_gui.main_function.append(('main_menu',main_menu))

#main function : 1
def withdraw(root,phase,USER_NAME,cell_num = None):
    global current_page
    print('withdraw : phase ' + str(phase))
    if phase == 0:
        stss_gui.Draw_Page(root,1)
        stss_gui.Arrange_ToolButton(root)
        stss_gui.wait_push(root,'tool_select',withdraw,phase,USER_NAME)

    elif phase == 1:
        print('selected : ' + str(cell_num))

        #CLI更新

        #ボタン非表示

        #回転

        #ドア開く

        #待機

        #管理ファイル更新

        #finish
        current_page = 0

stss_gui.flags['tool_select'] = (False,None)
stss_gui.main_function.append(('withdraw',withdraw))

#main function : 2
def deposit(SERIAL_NUMBER):
    #実装
    #
    #
    pass

stss_gui.flags['finish_deposit'] = (False,None)
stss_gui.main_function.append(('deposit',deposit))



#machine setting
nfc = nfcReader()

root = tkinter.Tk()
#
#
#
stss_gui.Draw_Page(root,0)

root.after(100,main_menu,root)

print('start')
root.mainloop()