import uiautomator2 as u2
d = u2.connect('ZX1G42CPJD')

import time
def sleep(t):
    time.sleep(t)
d.click(0.495, 0.899)
def sendMsg(i):
    d.click(0.495, 0.899)
    sleep(.2)
    d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[1]').click()
    if d.xpath('//*[@resource-id="com.tencent.mobileqq:id/elv_buddies"]/android.widget.LinearLayout[1]').exists:
        pass
    else:
        d.xpath('//*[@resource-id="com.tencent.mobileqq:id/elv_buddies"]/android.widget.RelativeLayout[2]/android.view.View[1]').click()
        sleep(.2)

    loc = d.xpath('//*[@resource-id="com.tencent.mobileqq:id/elv_buddies"]/android.widget.LinearLayout['+str(i)+']').center()
    bounds = d.xpath('//*[@resource-id="com.tencent.mobileqq:id/elv_buddies"]/android.widget.LinearLayout['+str(i)+']').info['bounds']
    height = bounds['bottom']-bounds['top']
    d.swipe(loc[0],loc[1],loc[0], loc[1]-height)


    d.xpath('//*[@resource-id="com.tencent.mobileqq:id/elv_buddies"]/android.widget.LinearLayout['+str(i)+']').click()
    sleep(.2)
    d(resourceId="com.tencent.mobileqq:id/txt", text="发消息").click()
    sleep(.2)
    d(resourceId="com.tencent.mobileqq:id/input").click()
    d.send_keys("测试文本", clear=True)
    sleep(.2)
    d(resourceId="com.tencent.mobileqq:id/cq9").click()
    sleep(.2)
    d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").click()

    pass
d.send_keys("123456", clear=True)