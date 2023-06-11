import os
import io
import json
import cv2 

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

def find_xy(screen, template):
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

def touch(x,y):
    os.system(f'{adb_path} -s {device_id} shell input tap {x} {y}')
