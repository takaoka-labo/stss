import tkinter
import pandas as pd

current_page = 0 # main menu = 0, main function page = each function number
main_function = []

buttons = {}

def button_on(num,next_page):
    global current_page
    current_page = next_page


def Arrange_ToolButton(root):
    #state.csvの情報を読む
    df = pd.read_csv('state.csv',header=None)
    df = df[df.iloc[:, 1] != -1]
    print(df)

    # 読み込んだ情報をもとに取り出し用のボタンを作成
    for index, row in df.iterrows():
        button = create_button(root,str(row.iloc[1]),str(row.iloc[2]),1)
        button.place(x=10 + index * 150, y=300)  # ボタンの位置を調整
        buttons[str(row.iloc[2])] = button

def create_button(root,num,text,next_page):
    Font = ("MSゴシック", 18, "bold")
    button = tkinter.Button(root, text=text,height=3, width=7, font=Font,command=lambda: button_on(num,next_page))
    buttons[text] = button
    return button