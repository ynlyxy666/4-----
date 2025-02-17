#coding=utf-8

import gui.helptext
import tkinter as tk
from PIL import Image
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
        msgbx=tk.Message(form3,text=info.about,font=('楷体',10),width=300)
        msgbx.pack(padx=30,pady=30)
        form3.resizable(False,False)
        cw(form3,360,220)
    
    def helptxt():
        form4=tk.Toplevel(form1)
        form4.title('帮助')
        ht=st.ScrolledText(form4)
        ht.config(state=tk.NORMAL)
        ht.insert(tk.END,text)
        ht.config(state=tk.DISABLED)
        ht.config(font=('Arial',15))
        ht.pack()
        form4.resizable(False,False)
        cw(form4,640,360)

    def quit():
        form1.destroy()
        sys.exit()

    #print(sys.path)
    run()
    form1=tk.Tk()
    form1.title('课表生成')
    style = ttk.Style()
    style.theme_use('alt')
    form1.resizable(False,False)
    cw(form1,640,360)
    menu1=tk.Menu(form1,tearoff=False)
    form1.config(menu=menu1)
    menu1_1=tk.Menu(menu1,tearoff=False)
    menu1_1.add_command(label='退出',command=quit)
    menu1.add_cascade(label='文件',menu=menu1_1)
    menu1.add_command(label='帮助',command=helptxt)
    menu1.add_command(label='关于',command=About)
    bt1=ttk.Button(form1,text='开始',command=About)
    bt1.pack(padx=4)
    form1.protocol('WM_DELETE_WINDOW', quit)
    form1.mainloop()
