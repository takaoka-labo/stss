#from .stss_nfc import *
import stss_gui, stss_nfc, stss_motor, stss_csv
import tkinter
import time

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
        try:
            NFC_TYPE,string = nfc.get_data_v2()
            #print(string)
            #degugging
            #func_mode = int(input('enter function_number'))
            func_mode = NFC_TYPE
            #arg = NFC_arg_debug
            arg = string
            current_page = func_mode
            stss_gui.main_function[func_mode][1](root,0,arg) # start each function from phase : 0
        except Exception as e:
            print(e)
            stss_gui.after_id = root.after(200,main_menu,root)
    else:
        stss_gui.after_id = root.after(200,main_menu,root)

stss_gui.main_function.append(('main_menu',main_menu))

#main function : 1
def withdraw(root,phase,*arg): # 0:USER_NAME 1:cell_num
    print('withdraw : phase ' + str(phase))
    if phase == 0:
        stss_gui.Draw_Page(root,1)
        stss_gui.Arrange_ToolButton(root)
        stss_gui.cancel_button(root,stss_gui.TOOL_SELECT)
        stss_gui.wait_push(root,stss_gui.TOOL_SELECT,withdraw,phase,arg[0])

    elif phase == 1:
        print(arg[0])
        if arg[0][1] != stss_gui.cancel:

            print('selected cell_ID: ' + str(arg[0][1]))
            #CLI更新
            stss_gui.gui[stss_gui.P1_CLI].update_text(0.,'please wait...')

            #ボタン非表示
            stss_gui.gui[stss_gui.P1_BUTTON_ARRAY].destroy()
            
            #回転
            revolver.position(int(arg[0][1]) - 1)

            #ドア開く
            door.open()

            #待機
            time.sleep(5)
            door.close()

            #管理ファイル更新
            #print(USER_NAME[0])
            csv_master.update_withdraw(arg[0][0],int(arg[0][1]) - 1)

        else:
            #ボタン非表示
            stss_gui.gui[stss_gui.P1_BUTTON_ARRAY].destroy()

        #finish
        stss_gui.return_main_menu(root)

stss_gui.flags[stss_gui.TOOL_SELECT] = (False,None)
stss_gui.main_function.append(('withdraw',withdraw))

#main function : 2
def deposit(root,phase,*arg): # 0:SERIAL_NUMBER 1:cell_num
    global current_page
    print(arg)
    if phase == 0:
        stss_gui.Draw_Page(root,2)
        
        #CLI更新
        stss_gui.gui[stss_gui.P2_CLI].update_text(0.,'please wait...')

        #state.csvからcell_num取得
        cell_num = csv_master.search_vacant_cell()
        print('cell_ID : ' + str(cell_num + 1))

        #回転
        revolver.position(cell_num)

        #CLI更新
        stss_gui.gui[stss_gui.P2_CLI].update_text(tkinter.END,'\nopen')
        
        #ドア開く
        door.open()

        #ボタン表示
        stss_gui.check_button(root)
        
        #GUI操作待ち
        stss_gui.wait_push(root,stss_gui.FINISH_DEPOSIT,deposit,phase,arg[0],cell_num)

    elif phase == 1:
        #管理ファイル更新
        print('arg = ')
        print(*arg)
        temp, *_ = arg
        door.close()
        csv_master.update_deposit(temp[0], temp[1])

        #finish
        stss_gui.return_main_menu(root)

stss_gui.flags[stss_gui.FINISH_DEPOSIT] = (False,None)
stss_gui.main_function.append(('deposit',deposit))


#machine setting
nfc = stss_nfc.nfcReader()
stss_motor.setting('/dev/ttyUSB0')
revolver = stss_motor.revolver(1,1000000)
door = stss_motor.door(2,1000000)

### mainloop
root = tkinter.Tk()
root.title('STSS - Smart Tool Strage System -')
root.geometry('500x400')
#
stss_gui.Draw_Page(root,0)
root.after(200,main_menu,root)
root.mainloop()
#

stss_motor.close()