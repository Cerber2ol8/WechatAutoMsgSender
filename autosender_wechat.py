import time
import random
import uiautomator2 as u2
import configparser
import os

debug = True
file = './text.txt'
text = []

def loadCfg():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    return config



def connect(cfg, mode='ip', Emu=True):
    
    serial = config['device']['serial']
    ip = config['device']['ip']
    if mode== 'ip':
        if Emu:
            r = os.system('adb connect '+ ip +':7555')
        else:
            r = os.system('adb connect '+ ip)
        print(r)
        d = u2.connect(ip)
        return d
    elif mode=='serial':
        d = u2.connect(serial)
        return d
    else:
        print('连接设备失败（参数错误）')
        return
def readText(file):
    with open(file) as f: 
        lines = f.readlines()
        return lines
def selectText(text):
    n = random.randint(0,len(text)-1)
    return text[n]



def sleep(t):
    time.sleep(t)
def getContrats():
    sleep(.2)
    contracts = d.xpath('//*[@resource-id="com.tencent.mm:id/czl"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.LinearLayout[1]')
    print('trun to contracts')
    contracts.click()
     
        
def sendMsg():
    button = d.xpath('//*[@resource-id="com.tencent.mm:id/b2b"]')
    print('button exists status:' + str(button.exists))
    if button.exists:
        d(resourceId="com.tencent.mm:id/b2b").click()
        d(resourceId="com.tencent.mm:id/g78").click()
        n = random.randint(0,len(lines)-1)
        text = lines[n]
        if debug:
            print(text)
        else:
            d.send_keys(text, clear=True)
            d(resourceId="com.tencent.mm:id/anv").click()
        d(resourceId="com.tencent.mm:id/rr").click()
    else:
        d(resourceId="com.tencent.mm:id/dm").click()
#elements =   d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]')


#elem = d(resourceId="com.tencent.mm:id/dy5",instance=4)

    
#elem.click()

def main(i,j):
    getContrats()
    h1 = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]').info
    h1 = h1['bounds']['bottom'] - h1['bounds']['top']
    h2 = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]').info
    h2 = h2['bounds']['bottom'] - h2['bounds']['top']
    c1 = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]').center()
    c2 = d.xpath('//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]').center()
    print(h1,h2,c1,c2)
    AtoSharp = 27
    while(True):
        #a-z + #
        if i<=AtoSharp:
            plist = '//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout[' + str(i) + ']'
            exists = d.xpath(plist).exists
            if exists:
                print('No.' + str(i) + 'Element Exists, Now Searching Friends...')
                print(plist)
                while(True):
                    path = '//*[@resource-id="com.tencent.mm:id/f4"]/android.widget.LinearLayout['+str(i)+']/android.widget.LinearLayout['+str(j)+']'
                    f = d.xpath(path)
                    if f.exists:
                        print('No.' + str(i) + 'Element Exists, Now Sending Message...')
                        print(path)
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





#main()
if __name__ == '__main__': 
    config = loadCfg()
    i = config.getint('layout','layout1')
    j = config.getint('layout','layout2')
    print(i,j)
    d = connect(cfg=config, mode='ip')
    print(d)
    #main(i,j)
