from collections import namedtuple
from re import L
import time
import uiautomator2 as u2
from main import *
from tools import *
import configparser

def loadCfg():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    return config

config = loadCfg()


def sleep(t):
    time.sleep(t)
global preIndex
global preName
global preChar
global reachBottom
global viewList

preIndex = -1
preName = ''
preChar = ''
reachBottom = False


def getItem(viewList, index):
    """返回指定序号的Item"""
    result = viewList.child(className='android.widget.LinearLayout',index=index)
    return result
def getName(item):
    """返回对应的Item文本内容"""
    if item.child(resourceId='com.tencent.mm:id/dy5').exists:
        result = item.child(resourceId='com.tencent.mm:id/dy5').info['text']
        return result
    else:
        return

def getChar(viewList):
    c = viewList.child(className='android.widget.TextView',resourceId='com.tencent.mm:id/b2x')
    return c

def getBounds(obj):
    """return [left,right,top,bottom]"""
    b = obj.info['bounds']
    return b
    
def findItem(viewList):
    """return list of uiautomator selector UiObject"""
    """找到当前页面所有的Item"""
    itemList = []
    for i in range(10):
        if i>0:
            newItem = getItem(viewList,i)
            if newItem.exists and newItem not in itemList:
                #print(i)
                itemList.append(newItem)
    print(str(len(itemList)) + ' items found')
    return itemList


def getContrats():
    global d
    sleep(.2)
    print('trun to contracts')
    viewList = d(className='android.widget.ListView',resourceId='com.tencent.mm:id/f4')
    if not viewList.exists:
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


def sendMsg(item):
    global preName
    preName = getName(item)
    item.click()
    sleep(2.5)
    button = d.xpath('//*[@resource-id="com.tencent.mm:id/b2b"]')
    print('button exists status:' + str(button.exists))
    if button.exists:
        d(resourceId="com.tencent.mm:id/b2b").click()
        sleep(.5)
        d(resourceId="com.tencent.mm:id/g78").click()
        sleep(.5)

        if debug:
            t = selectText(text)
            d.send_keys(t, clear=True)
            sleep(.5)
            #d(resourceId="com.tencent.mm:id/anv").click()
            d.send_keys('', clear=True)
            sleep(.5)
        else:
            t = selectText(text)
            d.send_keys(t, clear=True)
            sleep(.5)
            d(resourceId="com.tencent.mm:id/anv").click()
            sleep(.5)
        print("给" + preName + "发送了信息")
        d(resourceId="com.tencent.mm:id/rr").click()
        sleep(1)
    else:
        d(resourceId="com.tencent.mm:id/dm").click()
        sleep(1)

    getContrats()
    
def reToContracts():
    d.xpath('//*[@resource-id="com.tencent.mm:id/czl"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.LinearLayout[1]').click()
    sleep(.3)
    
def checkLoc(item):
    loc = item.center()
    
def turnTop():
    rect = d.xpath('//*[@resource-id="com.tencent.mm:id/fl"]').info['bounds']
    print('回到顶端')
    px = int((rect['left'] + rect['right'])/2)
    dy = int((rect['bottom']-rect['top'])/29)
    py = rect['top'] + dy
    print(px,py)
    d.click(px, py)
    sleep(.3)

def swipe(viewList,item):
    px,py = item.center()
    ex,ey = int((getBounds(viewList)['left']+getBounds(viewList)['right'])/2),getBounds(viewList)['top']
    item.drag_to(ex,ey, duration=0.3)
    print("(" + str(px) + ',' + str(py) + ') --> ( ' + str(ex) + ',' + str(ey) + ')')
    sleep(.5)
    
def ifReachBottom(viewList):
    if viewList.child(className='android.widget.FrameLayout').exists:
        global reachBottom
        reachBottom = True
        return True
    else:
        reachBottom = False
        return False


def app(device):
    global d 
    d = device
    global nameList
    global preNameList
    nameList = []
    preNameList = []
    getContrats()
    while(True):
        viewList = d(className='android.widget.ListView',resourceId='com.tencent.mm:id/f4')
        l = findItem(viewList = d(className='android.widget.ListView',resourceId='com.tencent.mm:id/f4'))
        nameList = []
        for item in l:
            name = getName(item)
            if name not in preNameList:
                nameList.append(name)
                sendMsg(item)
        if not ifReachBottom(viewList):
            #计算滑动的距离
            child = l[len(l)-1]
            ex,ey = int((getBounds(viewList)['left']+getBounds(viewList)['right'])/2),getBounds(viewList)['top']
            child.drag_to(ex,ey, duration=.7)
            sleep(1)
        else:
            
            print('reach bottom')

        preNameList = nameList


if __name__ == '__main__':
    # d = u2.connect('127.0.0.1')
    # app()
    de = config.getboolean('debug','debug')
    print(de)
