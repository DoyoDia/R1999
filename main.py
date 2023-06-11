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
        if time.time() - start_time > 60:
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
        break

