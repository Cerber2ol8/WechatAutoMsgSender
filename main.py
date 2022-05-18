from asyncio.tasks import wait_for
from logging import exception
from math import tau
from re import L, S
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import sender
import time
import random
import uiautomator2 as u2
import configparser
import os
from tools import *
import ctypes, sys
import App



file = './text.txt'
text = []

def loadCfg():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    return config

config = loadCfg()

def system(cmd):
    reply = os.popen(cmd)
    context = reply.read()
    return context

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
admin = is_admin()
def connect(cfg, mode='ip', Emu=True):
    print('正在连接设备...')
    serial = config['device']['serial']
    ip = config['device']['ip']
    if mode== 'ip':
        if Emu:
            r = system('adb connect '+ ip +':7555')
        else:
            r = system('adb connect '+ ip)
        print(r)
        r = system('python3 -m uiautomator2 init')
        print(r)
        return u2.connect(ip)
    elif mode=='serial':
        r = system('python3 -m uiautomator2 init')
        print(r)
        return u2.connect(serial)
    else:
        print('连接设备失败（参数错误）')
        return

def readText(file):
    with open(file,encoding='utf-8') as f: 
        lines = f.readlines()
        #print(lines)
        return lines
def selectText(text):
    n = random.randint(0,len(text)-1)
    return text[n]

text = readText(file)

def sleep(t):
    time.sleep(t)

#elements =   d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]')


#elem = d(resourceId="com.tencent.mm:id/dy5",instance=4)

    
#elem.click()

def main(i,j):
    def trunTop():
        rect = d.xpath('//*[@resource-id="com.tencent.mm:id/fl"]').info['bounds']
        print('回到顶端')
        px = int((rect['left'] + rect['right'])/2)
        dy = int((rect['bottom']-rect['top'])/29)
        py = rect['top'] + dy
        print(px,py)
        d.click(px, py)
        sleep(.3)

    def getWindowBounds():
        #获取滑动栏控件窗口位置
        b = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]').info['bounds']
        bounds = [b['left'],b['right'],b['top'],b['bottom']]
        return bounds


    def getContrats():
        sleep(.2)
        print('trun to contracts')
        while(True):
            contracts = d.xpath('//*[@resource-id="com.tencent.mm:id/czl"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.LinearLayout[1]')
            if contracts.exists:
                contracts.click()
                break
            return_button = d(resourceId="com.tencent.mm:id/rr")
            if  return_button.exists:
                return_button.click()
                sleep(.3)
                contracts.click()
                sleep(.3)
                break
            print('无法识别当前页面，请手动回到通讯录页面')
            sleep(3)


        
            
    def sendMsg():
        sleep(.4)
        button = d.xpath('//*[@resource-id="com.tencent.mm:id/b2b"]')
        print('button exists status:' + str(button.exists))
        if button.exists:
            d(resourceId="com.tencent.mm:id/b2b").click()
            sleep(.3)
            d(resourceId="com.tencent.mm:id/g78").click()
            sleep(.3)
            t = selectText(text)
            d.send_keys(t, clear=True)
            if debug:
                pass
            else:
                d(resourceId="com.tencent.mm:id/anv").click()
                sleep(.3)
            print('向用户[' + str(i) +'][' + str(j) + ']发送了消息： ' + t )
            d(resourceId="com.tencent.mm:id/rr").click()
            sleep(.2)
        else:
            d(resourceId="com.tencent.mm:id/dm").click()
            sleep(.2)

    getContrats() 
    l = '//*[@resource-id="com.tencent.mm:id/f4"]'

    if d(resourceId="com.tencent.mm:id/a14").exists:
        h1 = d(resourceId="com.tencent.mm:id/a14").info
    elif d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]').exists:
        h1 = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]').info
    else:
        print('没有识别到元素,任务中断')
        global workThread
        workThread.terminate()
    h1 = h1['bounds']['bottom'] - h1['bounds']['top']
    h2 = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]').info
    h2 = h2['bounds']['bottom'] - h2['bounds']['top']
    AtoSharp = 27
    while(True):
        #a-z + #
        if i<=AtoSharp:
            plist = '//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[' + str(i) + ']'
            exists = d.xpath(plist).exists
            if exists:
                print('No.' + str(i) + 'Element Exists, Now Searching Friends...')
                #print(plist)
                while(True):
                    path = '//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout['+str(i)+']/android.widget.LinearLayout['+str(j)+']'
                    f = d.xpath(path)
                    if f.exists:
                        print('No.' + str(i) + 'Element Exists, Now Sending Message...')
                        #print(path)
                        c = d.xpath(path).center()
                        d.xpath(path).click()
                        sleep(.2)
                        sendMsg()
                        getContrats()
                        d.swipe(c[0],c[1],c[0], c[1]-h2)
                        config['layout']['layout1'] = str(i)
                        config['layout']['layout2'] = str(j)
                        with open('./config.ini', 'w') as configfile:
                            config.write(configfile)
                        j+=1
                    else:
                        j=1
                        break
                pc = d.xpath(plist).center()
                d.swipe(pc[0],pc[1],pc[0], pc[1]-h1)
            else:
                print('No.' + str(i) + 'Element Not Found')
            i+=1
        else:
            break
    print('发送完成！')


def pause():
    while(IF_PAUSE):
        sleep(.5)

def connect_clicked():
    def func():
        global d
        d = connect(cfg=config, mode='ip')
        if d:
            global connected
            connected = True
            print(d)
        else:
            print('初始化设备失败')
            sys.exit()
    global connectThread
    connectThread = wThread(func=func)
    connectThread.start()


def start_clicked():
    def func():
        # try:
        #     print(connected)
        #     global d
        #     if d:
        #         if connected:
        #             print('开始任务')
        #             App.app(d)
        #         else:
        #             print('还没有连接设备，请先连接设备')
        #     else:
        #         print('初始化设备失败')
        #         sys.exit()
        # except Exception as e:
        #     print('发生异常:' + str(e) + '，任务终止')
        #     global workThread
        #     workThread.terminate()
        #     #sys.exit()
        # finally:
        #     pass
        print(connected)
        global d
        if d:
            if connected:
                print('开始任务')
                App.app(d)
            else:
                print('还没有连接设备，请先连接设备')
        else:
            print('初始化设备失败')
            sys.exit()
    global workThread
    workThread = wThread(func=func)
    workThread.start()
    global running
    running = True

def refresh_clicked():
    global i,j
    i = 1
    j = 0
    config['layout']['layout1'] = str(i)
    config['layout']['layout2'] = str(j)
    print('重新计数')
    with open('./config.ini', 'w') as configfile:
        config.write(configfile)

def reset_clicked():
    def func():
        r = system('python -m uiautomator2 init')
        print(r)
    global resetThread
    resetThread = wThread(func=func)
    resetThread.start()

def stop_clicked():
    global running
    if running:
        global workThread
        workThread.terminate()
        print('已停止线程')
    else:
        print('任务未启动')

def check_env():
    r = system('python -V')
    if 'Python' in r:
        print('已安装' + r + '，无需重新安装')
        return True
    else:
        print(r)
        return False
def install_clicked():
    global admin



    if not check_env():
        if admin:
            os.system('python-3.6.7-amd64.exe')
        else:
            print('将python添加到PATH需要管理员权限！')
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                exit()
            else:#in python2.x
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)


        

def setup_clicked():
    import getpass
    user_name = getpass.getuser() # 获取当前用户名
    path = 'C:\\Users\\' + user_name + '\\pip\\'
    if not os.path.exists (path):
        os.mkdir(path)
    os.system('copy .\\pip.ini ' + path + 'pip.ini')

    with open('./setup.bat',encoding='utf-8') as f: 
        lines = f.readlines()
        for i in range(len(lines)):
            print(lines[i])
            r = system(lines[i])
            print(r)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = sender.Ui_MainWindow()
    ui.setupUi(MainWindow)
    if not admin:
        from PyQt5 import QtCore
        ui.pushButton_5.setText(QtCore.QCoreApplication.translate("MainWindow", "安装python(需要管理员权限)"))
    MainWindow.show()
    
    
    global i,j
    i = config.getint('layout','layout1')
    j = config.getint('layout','layout2')

    if debug:
        print('DEBUG 模式，只会模拟过程，但不发送消息')

    ui.pushButton.clicked.connect(connect_clicked)
    ui.pushButton_2.clicked.connect(start_clicked)
    ui.pushButton_3.clicked.connect(reset_clicked)
    ui.pushButton_4.clicked.connect(stop_clicked)
    ui.pushButton_5.clicked.connect(install_clicked)
    ui.pushButton_6.clicked.connect(setup_clicked)
    sys.exit(app.exec_())
