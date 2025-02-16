这个程序为参加2025年“领航杯”江苏省中小学生信息素养比赛而制作，完全开源。

源代码运行环境：
python3.10+
Windows10+
pip24.3.1+
pyqt5

运行方法：
1. 安装python3.10,推荐安装python3.12+
2. 安装pip23.1.2+推荐安装pip24+
3. 安装pyqt5：python -m pip install pyqt5
4. 运行main.py

文件说明：
1. main.py为程序启动器
2. ".vscode"为vscode的配置文件
3. "辅助程序“为代码编写过程中使用的自己编写的小工具
4. "lib"为程序使用的库
5. "gif.gif"为程序启动画面
=== lib ===
1. "CenterWindow.py"为居中窗口的工具
2. "info.py"收录了程序使用的所有长字符串
4. "StartupMovie.py"为程序启动画面
5. "help.dat"为帮助文件

打包指令：
pyinstaller -F -w --add-data "gif.gif;." --add-data "tray.png;." main.pyw