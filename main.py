import os
import json
import pyadb
import r1999path
import time
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
        if time.time() - start_time > 60: #这样写不好，万一出下载时间过久就会直接退出应该检验一下是不是在loading或者应用在前台但是是预期之外的事
            print('超时，未匹配到任何模板图像')
            break
        else:
            time.sleep(1)
    elif status == 'login':
        r1999path.login()
        break
    elif status == 'title':
        #标题界面瞎点一下
        api.touch(939,455)
        time.sleep(1)
    elif status == 'notmenu2':
        print('action:notmenu2')
        #返回菜单
        api.touch(48,48)
        time.sleep(1)
    elif status == 'notmenu':
        print('action:notmenu')
        #返回菜单
        api.touch(48,48)
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
x,y=api.crop_match_template('img/NO1xCCO.png', 0, 186, 1280, 70)
print(x,y)
#if not 
print('先写到这儿')

