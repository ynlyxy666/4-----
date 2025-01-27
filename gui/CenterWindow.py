import tkinter as tk

def center_window(root, width, height):
    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口左上角的x和y坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置
    root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title('主界面')
    root.resizable(False, False)

    # 设置窗口大小为640x360，并将其定位在屏幕中心
    center_window(root, 640, 360)

    # 运行主循环
    root.mainloop()