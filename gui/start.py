#coding=utf-8

import tkinter as tk
from PIL import Image, ImageTk
import gui.info as info
import tooltip, threading
import tkinter.ttk as ttk
from gui.StartupMovie import run
import tkinter.scrolledtext as st
import os,sys, ctypes
from gui.CenterWindow import center_window as cw
from pygame import mixer
from multiprocessing import Process

# 新增DPI强制缩放设置
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def music():
    mixer.init()
    print("init success")
    mixer.music.load("bgm.ogg")
    print('src file loaded')
    mixer.music.play(-1)
    print('play')
    mixer.music.set_volume(0.5)
    print('set volume')

def gui():
    def get_path(relative_path):
        try:
            base_path = sys._MEIPASS # pyinstaller打包后的路径
        except AttributeError:
            base_path = os.path.abspath(".") # 当前工作目录的路径

        return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

    def helptxt():
        form3=tk.Toplevel(form1)
        form3.title('作者信息')
        msgbx=tk.Message(form3,text=info.about,font=('楷体',12),width=300, bg='#f0f0f0')
        msgbx.pack(padx=30,pady=30)
        form3.resizable(False,False)
        cw(form3,360,220)
    
    def helpcust():
        form6=tk.Toplevel(form1)
        form6.title('开发人员说明')
        menu=tk.Menu(form1,tearoff=False, font=('微软雅黑', 12))
        form6.config(menu=menu)
        menu1=tk.Menu(menu,tearoff=False, font=('微软雅黑', 12))
        menu1.add_command(label='退出',command=quit)
        menu.add_cascade(label='文件',menu=menu1_1)
        ht=st.ScrolledText(form6, bg='#f0f0f0', font=('微软雅黑',14))
        ht.config(state=tk.NORMAL)
        ht.insert(tk.END,info.helpcus)
        ht.config(state=tk.DISABLED)
        ht.pack(padx=20, pady=20)
        form6.resizable(False,False)
        cw(form6,640,360)

    def About():
        form4=tk.Toplevel(form1)
        form4.title('开发人员说明')
        menu=tk.Menu(form1,tearoff=False, font=('微软雅黑', 12))
        form4.config(menu=menu)
        menu1=tk.Menu(menu,tearoff=False, font=('微软雅黑', 12))
        menu1.add_command(label='退出',command=quit)
        menu.add_cascade(label='文件',menu=menu1_1)
        ht=st.ScrolledText(form4, bg='#f0f0f0', font=('微软雅黑',14))
        ht.config(state=tk.NORMAL)
        ht.insert(tk.END,info.helpdev)
        ht.config(state=tk.DISABLED)
        ht.pack(padx=20, pady=20)
        form4.resizable(False,False)
        cw(form4,640,360)

    def advanced():
        form5=tk.Toplevel(form1)
        form5.title('高级设置')
        form5.resizable(False,False)
        cw(form5,640,360)

    def quit():
        form1.destroy()
        sys.exit()


    #run()

    stmv = Process(target=run)
    #stmv.start()

    try:
        mixer.init()
        mixer.music.load("bgm.ogg")
        mixer.music.play(-1)
        mixer.music.set_volume(0.5)
        print("音乐老师，走！")
    except Exception as e:
        print("音乐走起失败")

    #stmv.join()

    ## 启用高DPI缩放支持
    form1=tk.Tk()
    dpi = form1.tk.call('tk', 'scaling')
    dpi2 = 1/dpi  # '1i'表示1英寸
    print("系统DPI:", dpi)
    #SCALE_FACTOR = dpi / 128  # 计算缩放比例
    form1.call('tk', 'scaling', dpi)  # 设置缩放因子，可以根据需要调整
    form1.title('课表生成')
    form1.resizable(False,False)
    cw(form1,640,360)

    bg_image_path = get_path('src/bg2.jpg') # 设置背景图片
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    canvas = tk.Canvas(form1, width=bg_image.width, height=bg_image.height)# 创建Canvas来显示背景图片
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')# 在Canvas上绘制背景图片
    
    white_box = tk.Label(form1, bg='white', width=20, height=18)  # 设置固定宽度和高度
    white_box.place(relx=1.0, rely=0.0, x=-20, y=20, anchor='ne')
    white_box.pack_propagate(False)  # 禁止白框随内容自动调整大小

    style = ttk.Style()  # 使用更美观的按钮样式
    style.configure('TButton', font=('楷体', 12), foreground='black', background='lightgray', borderwidth=0)  # 修改字体为楷体，并去除边框

    # 新增：自定义LabelFrame样式，设置背景为白色
    style.configure('White.TLabelframe', background='white')
    style.configure('White.TLabelframe.Label', background='white', font=('微软雅黑', 10))

    # 在白色框上放置一个LabelFrame，并应用自定义样式
    label_frame = ttk.LabelFrame(white_box, text="使用须知", padding=(10, 5), style='White.TLabelframe')
    label_frame.place(relx=0.5, rely=0.43, anchor='center', width=130, height=260)  # 固定位置和大小

    # 在LabelFrame内添加文字，并设置自动换行
    info_label = tk.Label(label_frame, text="生成前请您先点击下方的高级设置按钮查看和修改设置。\n==========\n本程序基于算法生成的课表仅供参考，需根据实际情况调整。", 
                      bg='white', font=('微软雅黑', 10), wraplength=100)  # 设置wraplength以实现自动换行
    info_label.pack(pady=5)

    canvas.create_text(100, 50, text='欢迎', fill='black', font=('隶书', 32))# 在Canvas上绘制文字
    
    style = ttk.Style()# 使用更美观的按钮样式
    style.configure('TButton', font=('楷体', 12), foreground='black', background='lightgray', borderwidth=0)  # 修改字体为楷体，并去除边框

    bottom_left_button = ttk.Button(form1, text='音乐开/关', command=print, style='TButton')
    bottom_left_button.place(relx=0.0, rely=1.0, x=20, y=-39, anchor='sw')  # 左下角定位

    # 添加生成按钮
    generate_button = ttk.Button(form1, text='生成', command=lambda: print("生成按钮被点击"), style='TButton')  # 应用自定义样式
    generate_button.place(relx=1.0, rely=1.0, x=-30, y=-39, anchor='se')  # 调整x和y值以控制按钮的位置

    # 添加高级设置按钮
    advanced_icon_path = get_path('src/ico/advanced.png')  # 假设图标文件名为advanced_icon.png
    advanced_icon = tk.PhotoImage(file=advanced_icon_path)
    
    advanced_button = ttk.Button(form1, image=advanced_icon, command=advanced, style='TButton')
    advanced_button.image = advanced_icon  # 保持对图像对象的引用，防止被垃圾回收
    advanced_button.place(relx=1.0, rely=1.0, x=-130, y=-39, anchor='se')  # 调整x和y值以控制按钮的位置

    # 添加工具提示
    advanced_button_tooltip = tooltip.ToolTip(advanced_button, text="高级设置")

    menu1=tk.Menu(form1,tearoff=False, font=('微软雅黑', 12))
    form1.config(menu=menu1)
    
    menu1_1=tk.Menu(menu1,tearoff=False, font=('微软雅黑', 12))
    menu1_1.add_command(label='退出',command=quit)
    
    menu1.add_cascade(label='文件',menu=menu1_1)
    menu1.add_command(label='帮助',command=helpcust)
    
    menu1_2=tk.Menu(menu1,tearoff=False, font=('微软雅黑', 12))
    menu1_2.add_command(label='作者信息',command=helptxt)
    menu1_2.add_command(label='开发人员说明',command=About)
    
    menu1.add_cascade(label='关于',menu=menu1_2)

    form1.protocol('WM_DELETE_WINDOW', quit)
    form1.mainloop()