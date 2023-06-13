import os
import json
import time
import re

import pyadb
import r1999path
import api


# 读取config.json文件
with open('config.json', 'r') as f:
    config = json.load(f)

device = pyadb.is_adb_connected()
if not device:
    print("Error: 未连接设备，请回看上面的错误信息")
    exit(1)
r1999path.is_game_on()
start_time = time.time()
while True:
    status = r1999path.where_am_i()
    if status is None:
        if time.time() - start_time > 180: #这样写不好，万一出下载时间过久就会直接退出应该检验一下是不是在loading或者应用在前台但是是预期之外的事
            print('启动超时')
            time.sleep(1)
            break
        else:
            #点击屏幕中上方来确认可能的签到
            #api.touch(670,80)
            time.sleep(1)
    elif status == 'login':
        r1999path.login()
        break
    elif status == 'title':
        #标题界面瞎点一下
        api.touch(939,455)
        time.sleep(1)
    elif status == 'got':
        #获得界面瞎点一下
        api.touch(670,80)
        time.sleep(1)
    elif status == 'signin':
        #签到界面瞎点一下
        api.touch(382,159)
        time.sleep(1)
    elif status == 'close':
        #能关的界面点关闭
        xy=api.crop_match_template('img/close.png',640,0,640,720)
        api.touch(xy[0],xy[1])
        time.sleep(1)
    elif status == 'update':
        #更新界面点下载
        api.touch(807,459)
        time.sleep(1)
    elif status == 'notmenu2': #在签到界面点返回键竟然能给到签了，神奇
        print('action:notmenu2')
        #返回菜单
        api.touch(48,48)
        time.sleep(1)
    elif status == 'notmenu':
        print('action:notmenu')
        #返回菜单
        api.touch(48,48)
        time.sleep(1)
    elif status == 'nothome':
        print('action:nothome')
        #返回菜单
        api.touch(140,47)
        time.sleep(1)
    elif status == 'menu':
        print('开始任务')
        break

del pyadb#释放pyadb

#x,y=api.find('img/fight.png')
api.touch(1058,241)#点击战斗
time.sleep(3)
api.touch(303,650)#点击资源
time.sleep(3)
while True:
    result = api.crop_match_template('img/NO1xCCO.png', 0, 186, 1280, 70)
    if result is None:
        #意志解析不在第一个
        #打尘埃运动
        while True:
            result = api.crop_match_template('img/LP1xL2P.png', 0, 186, 1280, 70)
            if result is not None:
                api.touch(result[0], result[1])
                time.sleep(0.5)
                break
            else:
                api.swipe(600,500,200,200)
                time.sleep(0.5)
        break
    else:
        #就俩数要不干脆图像识别吧，OCR的单字识别也太烂了
        #text = api.corp_ocr(result[0]+130, 500, 70, 35)
        #number = int(''.join(re.findall(r'\d+', text)))
        parse = api.crop_match_template('img/org_2.png',result[0]+130, 500, 70, 35)
        if parse is not None:
            parsec_count= 2
        else:
            parse = api.crop_match_template('img/org_1.png',result[0]+130, 500, 70, 35)
        if parse is not None:
            parsec_count= 1
        else:
            parsec_count= 0
        print(parsec_count) 
        api.touch(result[0], result[1])
        time.sleep(1)
        break

while True:
    result = r1999path.find_episode(5)
    if result:
        api.touch(result[0],result[1])
        time.sleep(1)
        break
    else:
        api.swipe(417,1290,625,625)
    

print('先写到这儿')

