import tkinter
import pandas as pd

current_page = 0 # main menu = 0, main function page = each function number
main_function = []

buttons = {}
flags = {}
gui = {}

#flag tags
TOOL_SELECT = 'tool_select'
FINISH_DEPOSIT = 'finish_deposit'


#GUI widget names

#page 1
P1_CLI = 'p1_cli'

#GUI designs
CLI_BG = "#101010"

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
    button_panel = tkinter.Frame(root, width=200, height=50, bg='white')
    button_panel.place(x=0, y=100)
    # 読み込んだ情報をもとに取り出し用のボタンを作成
    for index, row in df.iterrows():
        button = create_button(button_panel, str(row.iloc[1]), str(row.iloc[2]), next_page = None, flag_name = 'tool_select')
        button.place(x=10 + index * 30, y=0)  # ボタンの位置を調整
        buttons[str(row.iloc[2])] = button
    #print('debug arrange_toolbutton')
    root.update()

def create_button(button_panel,num,text,next_page = None,flag_name = None):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(button_panel, text=text,height=3, width=7, font=Font,command=lambda: button_on(num,next_page,flag_name))
    buttons[text] = button
    return button

def destroy_button(button_panel):
    for button in buttons.values():
        button.destroy()
    buttons.clear()
    button_panel.destroy()

def check_button(root):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(root, text='check',height=3, width=7, font=Font,command=lambda: print("完了ボタン押した時のフラグ"))##フラグ処理？

def Draw_Page(root,page_num):
    if page_num == 0:
        pass

    elif page_num == 1:
        cli = CLI(root)
        gui[P1_CLI] = cli
        #
        #
        #
    
    root.update()

def cli_draw(frame,cli_text):
    text = tkinter.StringVar()
    text.set(cli_text)
    text_disp = tkinter.Label(frame,anchor="nw",width=100,height=8,foreground="#000000",background='#87cefa',textvariable=text,font=("MSゴシック", 20))
    text_disp.place(x=10,y=10)

def wait_push(root,flag_name,func,before_phase,*arg):
    global after_id
    
    if after_id != None:
        root.after_cancel(after_id)
    
    if flags[flag_name][0] == True:
        func(root, before_phase + 1, arg,cell_num = flags[flag_name][1])
    else:
        print(after_id)
        after_id = root.after(100,wait_push,root,flag_name,func,before_phase,*arg)

class CLI:
    def __init__(self,root):
        self.master = root
        self.frame = tkinter.Frame(root,width=20,height=10,padx = 5,pady=5,bg = CLI_BG,)
        self.frame.pack(side=tkinter.TOP,anchor=tkinter.N, expand=True, fill=tkinter.X )
        self.text = tkinter.Label(self.frame,text='text',anchor=tkinter.W,fg="#FFFFFF",bg = CLI_BG)
        self.text.pack(side=tkinter.TOP, anchor=tkinter.W,expand=True,padx=2,pady=2)

    def update_text(self,str):
        self.text["text"] = str
        self.frame.update
