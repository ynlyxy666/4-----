#coding=utf-8
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
from lib.StartupMovie import run
import time
from lib.CenterWindow import center_window as cw
import lib.info as info
import sys
import psutil
import threading


def bt1c():
    #bt1.config(text='只能打开一次的哦')
    #bt1.config(state='disabled')
    form2=tk.Toplevel(form1)
    form2.title('时间')
    cw(form2,640,360)
    lb1t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    lb1=ttk.Label(form2,text=lb1t,font=('Cascadia Code',10))
    lb1.pack(padx=30,pady=30)

def About():
    form3=tk.Toplevel(form1)
    form3.title('关于')
    msgbx=tk.Message(form3,text=info.about,font=('楷体',15),width=300)
    msgbx.pack(padx=30,pady=30)
    form3.resizable(False,False)
    cw(form3,360,220)
    
def help():
    form4=tk.Toplevel(form1)
    form4.title('帮助')
    ht=st.ScrolledText(form4)
    ht.config(state=tk.NORMAL)
    ht.insert(tk.END,info.help)
    ht.config(state=tk.DISABLED)
    ht.config(font=('Arial',15))
    ht.pack()
    form4.resizable(False,False)
    cw(form4,640,360)

def quit():
    form1.destroy()
    sys.exit()


if __name__ == '__main__': 
    run()
    form1=tk.Tk()
    form1.title('主界面')
    form1.resizable(False,False)
    cw(form1,640,360)
    menu1=tk.Menu(form1,tearoff=False)
    form1.config(menu=menu1)
    menu1_1=tk.Menu(menu1,tearoff=False)
    menu1_1.add_command(label='退出',command=quit)
    menu1.add_cascade(label='文件',menu=menu1_1)
    menu1.add_command(label='帮助',command=help)
    menu1.add_command(label='关于',command=About)
    main_title=ttk.Label(form1,text='主界面',font=('华文彩云',20))
    main_title.grid(row=0,column=0)
    bt1=ttk.Button(form1,text='打开一个界面',command=bt1c)
    bt1.grid(row=1,column=0)
    form1.mainloop()