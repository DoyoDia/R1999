import os
import json
import cv2
import numpy as np 

with open('config.json', 'r') as f:
    config = json.load(f)
adb_path = config['adb_path']
device_id = config['device_id'] 
def get_screen_shot():
    os.system(f'{adb_path} -s {device_id} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def is_img_on(screen, template):
    result = cv2.matchTemplate(template, screen, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 阈值
    if cv2.minMaxLoc(result)[1] >= threshold:
        return 1
    else:
        return 0

def find_xy(template):
    screen = get_screen_shot()
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #print("prob:", max_val)
    if max_val > 0.98:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        return center
    else:
        return False

# 匹配图像
def match_template(screen, template):
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6  # 阈值
    loc = np.where(result >= threshold)
    if len(loc[0]) > 0:
        return loc[1][0], loc[0][0]
    else:
        return None

# 裁剪截屏
def crop_screen(screen, x, y, w, h):
    return screen[y:y+h, x:x+w]

#裁屏匹配
def crop_match_template(template, x, y, w, h):
    screen = cv2.imread(get_screen_shot())
    template_img = cv2.imread(template)
    screen_corped = screen[y:y+h, x:x+w]
    result = cv2.matchTemplate(screen_corped , template_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6  # 阈值
    loc = np.where(result >= threshold)
    if len(loc[0]) > 0:
        # 在匹配结果上画框
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screen_corped, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imwrite('cache/result2.png', screen_corped)
        x=loc[1][0]+x 
        y=loc[0][0]+y
        return x, y
    else:
        return None

#adb相关
def touch(x,y):
    os.system(f'{adb_path} -s {device_id} shell input tap {x} {y}')

def swipe(x1,y1,x2,y2):
    os.system(f'{adb_path} -s {device_id} shell input swipe {x1} {y1} {x2} {y2}')

