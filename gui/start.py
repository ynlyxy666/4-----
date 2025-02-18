#coding=utf-8

import tkinter as tk
import gui.info as info
import tkinter.ttk as ttk
from gui.helptext import text
import tkinter.scrolledtext as st
import os,sys
from gui.CenterWindow import center_window as cw
from tkinter import filedialog, messagebox
import os
import sys

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

    def start_scheduling():
        # 这里可以添加生成课表的逻辑
        messagebox.showinfo("提示", "开始生成课表")

    def import_courses():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            # 这里可以添加导入课程信息的逻辑
            messagebox.showinfo("提示", f"导入了课程信息: {file_path}")

    def export_schedule():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            # 这里可以添加导出课表的逻辑
            messagebox.showinfo("提示", f"导出了课表: {file_path}")

    def preview_schedule():
        # 这里可以添加预览课表的逻辑
        messagebox.showinfo("提示", "预览课表")
    
    form1 = tk.Tk()
    form1.title('自动课表设计')
    style = ttk.Style()
    style.theme_use('alt')
    form1.resizable(False, False)
    cw(form1, 800, 600)
    menu1 = tk.Menu(form1, tearoff=False)
    form1.config(menu=menu1)
    menu1_1 = tk.Menu(menu1, tearoff=False)
    menu1_1.add_command(label='退出', command=quit)
    menu1.add_cascade(label='文件', menu=menu1_1)
    menu1.add_command(label='帮助', command=helptxt)
    menu1.add_command(label='关于', command=About)

    # 添加更多的控件
    ttk.Label(form1, text="课程名称:").grid(row=0, column=0, padx=10, pady=10)
    course_name_entry = ttk.Entry(form1)
    course_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(form1, text="课程时间:").grid(row=1, column=0, padx=10, pady=10)
    course_time_entry = ttk.Entry(form1)
    course_time_entry.grid(row=1, column=1, padx=10, pady=10)

    import_button = ttk.Button(form1, text='导入课程', command=import_courses)
    import_button.grid(row=2, column=0, padx=10, pady=10)

    export_button = ttk.Button(form1, text='导出课表', command=export_schedule)
    export_button.grid(row=2, column=1, padx=10, pady=10)

    preview_button = ttk.Button(form1, text='预览课表', command=preview_schedule)
    preview_button.grid(row=2, column=2, padx=10, pady=10)

    start_button = ttk.Button(form1, text='开始生成课表', command=start_scheduling)
    start_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    form1.protocol('WM_DELETE_WINDOW', quit)
    form1.mainloop()