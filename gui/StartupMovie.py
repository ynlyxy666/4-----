import time
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import QMainWindow, QSplashScreen
 
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径
 
    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径


class MySplashScreen(QSplashScreen):
    def __init__(self):
        super(MySplashScreen, self).__init__()
 
        # 新建动画
        self.movie = QMovie(get_path('gif.gif'))
        self.movie.frameChanged.connect(lambda: self.setPixmap(self.movie.currentPixmap()))
        self.movie.start()
 
    def mousePressEvent(self, QMouseEvent):
        pass
 
 
class LoadDataWorker(QObject):
    finished = pyqtSignal()
    message_signal = pyqtSignal(str)
 
    def __init__(self):
        super(LoadDataWorker, self).__init__()
 
    def run(self):
        for i in range(90):
            time.sleep(0.1)
            #self.message_signal.emit(f'加载中...{str(i * 10)}%')
        self.finished.emit()
 
 
class Form(QMainWindow):
    def __init__(self, splash):
        super(Form, self).__init__()
        self.resize(800, 600)
 
        self.splash = splash
 
        self.load_thread = QThread()
        self.load_worker = LoadDataWorker()
        self.load_worker.moveToThread(self.load_thread)
        self.load_thread.started.connect(self.load_worker.run)
        self.load_worker.message_signal.connect(self.set_message)
        self.load_worker.finished.connect(self.load_worker_finished)
        self.load_thread.start()
 
        while self.load_thread.isRunning():
            QtWidgets.qApp.processEvents()  # 不断刷新，保证动画流畅
 
        self.load_thread.deleteLater()
 
    def load_worker_finished(self):
        self.load_thread.quit()
        self.load_thread.wait()
 
    def set_message(self, message):
        self.splash.showMessage(message, Qt.AlignLeft | Qt.AlignBottom, Qt.white)
 
def run():
    import sys
    from PyQt5.QtWidgets import QApplication
 
    app = QApplication(sys.argv)
 
    splash = MySplashScreen()
    # splash.setPixmap(QPixmap(r'D:\图标\28c932975ab836b2d1939979db0fd8b8.jpg'))  # 设置背景图片
    splash.setFont(QFont('微软雅黑', 10))  # 设置字体
    splash.show()
 
    app.processEvents()  # 处理主进程，不卡顿
    form = Form(splash)
    #form.show()
    #splash.hide()
    splash.finish(form)  # 主界面加载完成后隐藏
    splash.movie.stop()  # 停止动画
    splash.deleteLater()
    #app.exec_() 


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
 
    app = QApplication(sys.argv)
 
    splash = MySplashScreen()
    # splash.setPixmap(QPixmap(r'D:\图标\28c932975ab836b2d1939979db0fd8b8.jpg'))  # 设置背景图片
    splash.setFont(QFont('微软雅黑', 10))  # 设置字体
    splash.show()
 
    app.processEvents()  # 处理主进程，不卡顿
    form = Form(splash)
    #form.show()
    #splash.hide()
    splash.finish(form)  # 主界面加载完成后隐藏
    splash.movie.stop()  # 停止动画
    splash.deleteLater()
    #app.exec_()
