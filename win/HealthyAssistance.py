import tkinter as tk
from tkinter import messagebox
from threading import Thread

import os
import core
import initial
import json


# core func definition
def prompt(msg):
    window = tk.Tk()
    window.withdraw()
    messagebox.showinfo("Notification",msg)
    window.destroy()

# id,pw window
class InfoWindow:
    def __init__(self):
        # show提示信息
        self.t = Thread(target=prompt, args=("首次使用，需要填写您的学号及密码",))
        self.t.start()

        self.root = tk.Tk()
        # set window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        root_width = 250
        root_height = 100
        x = (screen_width - root_width) / 2
        y = (screen_height - root_height) / 2
        self.root.geometry('%dx%d+%d+%d'%(root_width,root_height,x,y))

        # set title
        self.root.title('创建用户')
        # set icon
        self.root.iconbitmap(r'.\images\heart.ico')
        self.fm1 = tk.Frame(self.root)
        self.l1 = tk.Label(self.fm1,text='    学号:',font=('old',15),justify=tk.RIGHT)
        self.l1.pack()
        self.l2 = tk.Label(self.fm1,text='    密码:',font=('old',15),justify=tk.RIGHT)
        self.l2.pack()
        self.fm1.grid(row=0,column=0)

        
        self.fm2 = tk.Frame(self.root)
        # e1 学号
        self.e1 = tk.Entry(self.fm2,width=15)
        self.e1.pack()
        # e2 密码
        self.e2 = tk.Entry(self.fm2,width=15,show='*')
        self.e2.pack()
        self.fm2.grid(row=0,column=1)

        self.fm3 = tk.Frame(self.root)
        self.empty_label = tk.Label(self.fm3,text='               ').pack(side=tk.LEFT)
        self.b1 = tk.Button(self.fm3,text='创建',width=10,height=1,command=self.create_origin_file).pack(side=tk.LEFT)
        self.fm3.grid(row=1,column=0,columnspan=2)

        self.root.mainloop()
    
    def create_origin_file(self):
        # write origin file:
        id = self.e1.get()
        pw = self.e2.get()
        tmp = []
        tmp.append(id)
        tmp.append(pw)
        with open(r'.\data\origin.json','w') as f:
            json.dump(tmp,f)
        # for rewriting password.json
        if os.path.exists(r'.\data\password.json'):
            os.remove(r'.\data\password.json')
        
        prompt('Successfully save!')
        # show feedback
        self.root.destroy()




# 首次使用
if not os.path.exists(r'.\data\dirty'):
    with open(r'.\data\dirty','w') as f:
        f.write('Thanks for your choice.')

    declare_str = '''
        我是暨南大学18级计算机科学与技术的学生，
    本产品本着方便的目的，供大家食用。本软件使
    用过程中绝不泄露隐私等敏感信息，源代码已经
    公开在github上，供大家监督。
        最后，不得用本产品用作商业目的，本软件
    所有权为astzls213所有。如果喜欢作者可以添
    加作者微信打赏作者，1毛也可。
    '''
    root = tk.Tk()
    # set window size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root_width = 600
    root_height = 300
    x = (screen_width - root_width) / 2
    y = (screen_height - root_height) / 2
    root.geometry('%dx%d+%d+%d'%(root_width,root_height,x,y))
    # set title
    root.title('免责声明')
    # set icon
    root.iconbitmap(r'.\images\heart.ico')
    # set photo
    logo = tk.PhotoImage(file=r".\images\jnu.png")
    w1 = tk.Label(root, image=logo).pack(side="right")
    # set text
    w2 = tk.Label(root,
                  justify=tk.LEFT,
                  padx = 8,
                  text=declare_str,
                  font=('old',20)
                  ).pack(side="top")
    # set button
    b1 = tk.Button(root,
                    text='I agreed',
                    command=root.destroy,
                    width=10,
                    height=1
                    ).pack(side="bottom")

    root.mainloop()



# no origin file, create a window to get it.
if not os.path.exists(r'.\data\origin.json'):
    infoWindow = InfoWindow()


# no password file, init it.
if not os.path.exists(r'.\data\password.json'):
    t = Thread(target=prompt, args=('初次打卡需要获取必要信息,请稍后...',))
    t.start()
    status = initial.init()
    if not status:
        prompt('Internet选项->连接->局域网设置, 为LAN使用代理服务器（取消勾选）')

# get feedback
attendance = core.run()

# show attendance in windows, and exit
prompt(attendance)