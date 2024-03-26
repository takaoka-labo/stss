import tkinter
import pandas as pd

current_page = 0 # main menu = 0, main function page = each function number
main_function = []

buttons = {}
flags = {}
gui = {} #現在使用中のウィジェット

#flag tags
TOOL_SELECT = 'tool_select'
FINISH_DEPOSIT = 'finish_deposit'

#GUI widget names

#page 1
P1_CLI = 'p1_cli'
P1_BUTTON_ARRAY = 'p1_button_array'

#page 2
P2_CLI = 'p2_cli'
P2_CHECK_BUTTON = 'p2_check_button'

#GUI designs
CLI_BG = "#101010"

after_id = None

def button_on(num,next_page,flag_name):
    global current_page
    print('pushed ' + num)
    current_page = next_page if next_page != None else current_page
    flags[flag_name] = (True,num) if flags[flag_name][0] != None else flags[flag_name]

def Arrange_ToolButton(root):
    global gui
    #state.csvの情報を読む
    df = pd.read_csv('state.csv',header=None)
    df = df[df.iloc[:, 1] != -1]
    #print(df)
    button_panel = tkinter.Frame(root, width=500, height=100, bg='white',borderwidth=3)
    gui[P1_BUTTON_ARRAY] = button_panel

    # 読み込んだ情報をもとに取り出し用のボタンを作成
    for index, row in df.iterrows():
        button = create_button(button_panel, str(row.iloc[0]), str(row.iloc[2]), next_page = None, flag_name = TOOL_SELECT)
        button.place(x=10 + index * 30, y=0)  # ボタンの位置を調整
        buttons[str(row.iloc[2])] = button
    #print('debug arrange_toolbutton')
    button_panel.place(x=0, y=100)
    #button_panel.pack()
    root.update()

def create_button(button_panel,num,text,next_page = None,flag_name = None):
    Font = ("MSゴシック", 12, "bold")
    button = tkinter.Button(button_panel, text=text,height=3, width=6, font=Font,command=lambda: button_on(num,next_page,flag_name))
    buttons[text] = button
    return button

def destroy_button(button_panel):
    for button in buttons.values():
        button.destroy()
    buttons.clear()
    button_panel.destroy()

def check_button(root):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(root, text='check',height=3, width=7, font=Font,command=lambda: button_on('check',next_page = None,flag_name = FINISH_DEPOSIT))##フラグ処理？
    gui[P2_CHECK_BUTTON] = button
    button.place(x=0, y=100)

def Draw_Page(root,page_num):
    global gui
    #子ウィジェットの消去
    for child in root.winfo_children():
        child.destroy()
    #現在使用中のウィジェットは無し
    gui.clear()

    if page_num == 0:
        cli = CLI(root)
        gui[P1_CLI] = cli

    elif page_num == 1:
        cli = CLI(root)
        gui[P1_CLI] = cli
        
    elif page_num == 2:
        cli = CLI(root)
        gui[P2_CLI] = cli
    
    root.update()

def wait_push(root,flag_name,func,before_phase,*arg):
    global after_id
    #print(arg)
    if after_id != None:
        root.after_cancel(after_id)
    
    if flags[flag_name][0] == True:
        flags[flag_name] = (False,flags[flag_name][1])
        func(root, before_phase + 1, arg + (flags[flag_name][1],))
    else:
        #print(after_id)
        #print(arg)
        after_id = root.after(200,wait_push,root,flag_name,func,before_phase,*arg)

class CLI:
    def __init__(self,root):
        self.master = root
        #self.frame = tkinter.Frame(root,width=200,height=100,padx = 5,pady=5,bg = CLI_BG)
        self.text = tkinter.Text(root,fg="#FFFFFF",bg = CLI_BG,padx=5,pady=5,height=8)
        self.text.pack(side=tkinter.TOP)

        #self.frame.pack(side=tkinter.TOP,anchor=tkinter.N, expand=True, fill=tkinter.X )

    def update_text(self,position,str,reflesh = False):
        if reflesh == True:
            self.text.delete(0.,tkinter.END)
            
        self.text.insert(position,str)
        self.text.update()

def return_main_menu(root):
    global gui,current_page
    #子ウィジェットの消去
    for child in root.winfo_children():
        child.destroy()
    #現在使用中のウィジェットは無し
    gui.clear()

    current_page = 0
    Draw_Page(root,0)
    main_function[0][1](root)