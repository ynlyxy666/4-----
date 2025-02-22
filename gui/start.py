#coding=utf-8

import gui.helptext
import tkinter as tk
from PIL import Image, ImageTk
import gui.info as info
import tkinter.ttk as ttk
from PyQt5 import QtWidgets
from gui.helptext import text
from gui.StartupMovie import run
import tkinter.scrolledtext as st
from pystray import MenuItem, Menu
from PyQt5.QtGui import QFont, QMovie
import os,sys,time,psutil,pystray,threading
from gui.CenterWindow import center_window as cw
from PyQt5.QtWidgets import QMainWindow, QSplashScreen
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal

def gui():
    def get_path(relative_path):
        try:
            base_path = sys._MEIPASS # pyinstaller打包后的路径
        except AttributeError:
            base_path = os.path.abspath(".") # 当前工作目录的路径

        return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

    def About():
        form3=tk.Toplevel(form1)
        form3.title('关于')
        msgbx=tk.Message(form3,text=info.about,font=('楷体',12),width=300, bg='#f0f0f0')
        msgbx.pack(padx=30,pady=30)
        form3.resizable(False,False)
        cw(form3,360,220)
    
    def helptxt():
        form4=tk.Toplevel(form1)
        form4.title('帮助')
        menu=tk.Menu(form1,tearoff=False, font=('Arial', 12))
        form4.config(menu=menu)
        menu1=tk.Menu(menu,tearoff=False, font=('Arial', 12))
        menu1.add_command(label='退出',command=quit)
        menu.add_cascade(label='文件',menu=menu1_1)
        ht=st.ScrolledText(form4, bg='#f0f0f0', font=('Arial',14))
        ht.config(state=tk.NORMAL)
        ht.insert(tk.END,text)
        ht.config(state=tk.DISABLED)
        ht.pack(padx=20, pady=20)
        form4.resizable(False,False)
        cw(form4,640,360)

    def quit():
        form1.destroy()
        sys.exit()

    #run()
    form1=tk.Tk()
    form1.title('课表生成')
    form1.resizable(False,False)
    cw(form1,640,360)

    # 设置背景图片
    bg_image_path = get_path('src/bg2.jpg')
    bg_image = Image.open(bg_image_path)
    # 调整图片大小以适应窗口
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(form1, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # 添加白框
    white_box = tk.Label(form1, bg='white', width=20, height=18)
    white_box.place(relx=1.0, rely=0.0, x=-20, y=20, anchor='ne')

    # 添加欢迎二字
    welcome_label = tk.Label(form1, text='欢迎', font=('Arial', 32))
    welcome_label.place(relx=0.0, rely=0.0, x=20, y=20, anchor='nw')

    menu1=tk.Menu(form1,tearoff=False, font=('Arial', 12))
    form1.config(menu=menu1)
    menu1_1=tk.Menu(menu1,tearoff=False, font=('Arial', 12))
    menu1_1.add_command(label='退出',command=quit)
    menu1.add_cascade(label='文件',menu=menu1_1)
    menu1.add_command(label='帮助',command=helptxt)
    menu1.add_command(label='关于',command=About)

    # 使用更美观的按钮样式
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), foreground='blue', background='lightgray')
    #bt1=ttk.Button(form1,text='开始',command=About)
    #bt1.pack(padx=4)

    form1.protocol('WM_DELETE_WINDOW', quit)
    form1.mainloop()