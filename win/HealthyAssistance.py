import tkinter as tk
from tkinter import messagebox
import os
import core
import initial

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
    # set title
    root.title('免责声明')
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
                    text='OK',
                    command=root.destroy,
                    width=10,
                    height=1
                    ).pack(side="bottom")

    root.mainloop()



# no origin file, create a window to get it.
if not os.path.exists(r'.\data\origin.json'):
    messagebox.showinfo("提示","首次使用，需要填写您的学号及密码")
    root = tk.Tk()


# no password file, init it.
if not os.path.exists(r'.\data\password.json'):
    initial.init()


#attendance = core.run()

# show attendance in windows, and exit