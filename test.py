import os
import json
import time
import re

import pyadb
import r1999path
import api

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
        text = api.corp_ocr(result[0]+130, 500, 70, 35)
        number = int(''.join(re.findall(r'\d+', text)))
        print(number) 
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