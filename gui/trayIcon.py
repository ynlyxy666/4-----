import os
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import time
import sys
KeyboardInterrupt=1

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径
 
    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

def create_image():
    # 加载自定义的PNG图标文件
    img_path=get_path("tray.png")
    image = Image.open(img_path)
    return image

def on_clicked(icon, item):
    # 定义单击托盘图标时的操作
    if str(item) == '退出':
        icon.stop()
    else:
        print(f'{item} clicked')

def left_click(icon, item):
    # 定义按下托盘图标的左键时的操作
    print("123")

def background_task():
    # 后台任务
    while True:
        #print("后台任务运行中...")
        time.sleep(5)

def main():
    # 创建系统托盘图标
    icon = pystray.Icon("test",create_image())
    icon.menu = pystray.Menu(item('选项1', on_clicked),item('选项2', on_clicked),item('退出', on_clicked))
    icon.run_detached=left_click
    
    # 启动后台任务线程
    threading.Thread(target=background_task, daemon=True).start()

    # 运行系统托盘图标
    icon.run()

if __name__ == "__main__":
    main()