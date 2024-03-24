#from .stss_nfc import *
import stss_gui, stss_nfc, stss_motor, stss_csv
import tkinter

func_mode_debug = 1
NFC_arg_debug = 'nishiyama'

csv_master = stss_csv.csv_manager()

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
    frame = stss_gui.Draw_Page(root,1)
    if phase == 0:
        stss_gui.Arrange_ToolButton(root)
        stss_gui.wait_push(root,stss_gui.TOOL_SELECT,withdraw,phase,USER_NAME)

    elif phase == 1:
        print('selected : ' + str(cell_num))

        #CLI更新
        stss_gui.cli_draw(frame,'Please wait')
        

        #ボタン非表示
        stss_gui.destroy_button(frame)
        
        #回転

        #ドア開く

        #待機

        #管理ファイル更新
        stss_csv.update_state()
        stss_csv.update_manage()

        #finish
        current_page = 0

stss_gui.flags[stss_gui.TOOL_SELECT] = (False,None)
stss_gui.main_function.append(('withdraw',withdraw))

#main function : 2
def deposit(root,phase,SERIAL_NUMBER):
    global current_page
    if phase == 0:
        frame = stss_gui.Draw_Page(root,1)
        
        #CLI更新
        stss_gui.cli_draw(frame,'Please wait')

        #state.csvからcell_num取得
        csv_master.get_state()
        csv_master.get_manage()
                
        #回転

        #CLI更新
        stss_gui.cli_draw(frame,'Please wait')
        
        #ドア開く

        #ボタン表示
        stss_gui.check_button(root)
        
        #GUI操作待ち
        stss_gui.wait_push(root,stss_gui.FINISH_DEPOSIT,deposit,phase,SERIAL_NUMBER)
    elif phase == 1:
        #管理ファイル更新
        stss_csv.update_state()
        stss_csv.update_manage()

        #finish
        current_page = 0

stss_gui.flags[stss_gui.FINISH_DEPOSIT] = (False,None)
stss_gui.main_function.append(('deposit',deposit))


#machine setting
nfc = stss_nfc.nfcReader()
stss_motor.setting('/dev/ttyUSB0')

### mainloop
root = tkinter.Tk()
#
#
#
stss_gui.Draw_Page(root,0)
root.after(100,main_menu,root)
root.mainloop()
###

stss_motor.close()