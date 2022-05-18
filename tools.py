from types import FunctionType
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer, QThread, QTime
import time
from PyQt5.QtWidgets import QApplication
import configparser
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer, QThread, QTime
# import sys 
# from tools import EmittingStr
def loadCfg():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    return config

config = loadCfg()

debug = config.getboolean('debug','debug')
IF_PAUSE = False
connected = False
running = False



def sleep(t):
    time.sleep(t)


# 重定向信号
class EmittingStr(QtCore.QObject):
        textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

        def write(self, text):
            self.textWritten.emit(str(text))
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()



class MyThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self,data=None, parent=None):
        super(MyThread, self).__init__(parent)
        self.data = data

    def write(self, text):
        QApplication.processEvents()
        self.signalForText.emit(str(text))  # 发射信号

    def run(self, func):
        func()

class wThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self,data=None, parent=None,func=None):
        super(wThread, self).__init__(parent)
        self.data = data
        self.func = func

    def run(self):
        self.func()

class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)
 
    def write(self, text):
        self.newText.emit(str(text))
