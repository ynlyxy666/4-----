import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Notebook

form=tk.Tk()
form.geometry("640x360")
form.resizable(False,False)

# 大框
ntb=ttk.Notebook(form)
ntb.pack()
i1=ttk.Frame(ntb)
i2=ttk.Frame(ntb)
i3=ttk.Frame(ntb)

ntb.add(i1,text="123")
ntb.add(i2)
ntb.add(i3)
       
# 课程天数设置

form.mainloop()