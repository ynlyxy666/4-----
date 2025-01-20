import tkinter as tk
import tkinter.ttk as ttk
from lib.StartupMovie import run
import time
from lib.CenterWindow import center_window as cw

def bt1c():
    bt1.config(text='只能打开一次的哦')
    bt1.config(state='disabled')
    form2=tk.Toplevel(form1)
    form2.title('时间')
    cw(form2,640,360)
    lb1t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    lb1=ttk.Label(form2,text=lb1t,font=('Cascadia Code',10))
    lb1.pack(padx=30,pady=30)

def bt2c():
    form3=tk.Toplevel(form1)
    form3.title('关于')
    lb2=ttk.Label(form3,text='关于界面',font=('Cascadia Code',10))
    cw(form3,640,360)
    
if __name__ == '__main__': 
    #run()
    form1=tk.Tk()
    form1.title('主界面')
    #form1.geometry('640x360')
    form1.resizable(False,False)
    cw(form1,640,360)
    main_title=ttk.Label(form1,text='主界面',font=('Cascadia Code',20))
    main_title.grid(row=0,column=0)
    bt1=ttk.Button(form1,text='打开一个时间界面',command=bt1c)
    bt1.grid(row=1,column=0)
    bt2=ttk.Button(form1,text='打开一个关于界面',command=bt2c)
    bt2.grid(row=2,column=0)
    form1.mainloop()