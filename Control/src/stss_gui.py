import tkinter
import pandas as pd

current_page = 0 # main menu = 0, main function page = each function number
main_function = []

buttons = {}
flags = {}
#flag tags
TOOL_SELECT = 'tool_select'
FINISH_DEPOSIT = 'finish_deposit'


after_id = None

def button_on(num,next_page,flag_name):
    global current_page
    print('pushed ' + num)
    current_page = next_page if next_page != None else current_page
    flags[flag_name] = (True,num) if flags[flag_name][0] != None else flags[flag_name]

def Arrange_ToolButton(root):
    #state.csvの情報を読む
    df = pd.read_csv('state.csv',header=None)
    df = df[df.iloc[:, 1] != -1]
    #print(df)

    # 読み込んだ情報をもとに取り出し用のボタンを作成
    for index, row in df.iterrows():
        button = create_button(root, str(row.iloc[1]), str(row.iloc[2]), next_page = None, flag_name = 'tool_select')
        button.place(x=10 + index * 150, y=300)  # ボタンの位置を調整
        button.pack()
        buttons[str(row.iloc[2])] = button
    #print('debug arrange_toolbutton')
    root.update()

def create_button(root,num,text,next_page = None,flag_name = None):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(root, text=text,height=3, width=7, font=Font,command=lambda: button_on(num,next_page,flag_name))
    buttons[text] = button
    return button

def Draw_Page(root,page_num):
    pass

def wait_push(root,flag_name,func,before_phase,*arg):
    global after_id
    
    if after_id != None:
        root.after_cancel(after_id)
    
    if flags[flag_name][0] == True:
        func(root, before_phase + 1, arg,cell_num = flags[flag_name][1])
    else:
        print(after_id)
        after_id = root.after(100,wait_push,root,flag_name,func,before_phase,*arg)