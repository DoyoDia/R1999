import os
import json 
import api
import cv2
import time


# 读取config.json文件
with open('config.json', 'r') as f:
    config = json.load(f)
device_id = config['device_id'] 
def is_game_on():
    appid = 'com.shenlan.m.reverse1999'
    # 检测应用是否在前台
    with open('config.json', 'r') as f:
        config = json.load(f)
    adb_path = config['adb_path'] 
    command = (f'{adb_path} -s {device_id} '
               'shell dumpsys window windows')
    try:
        process = os.popen(command)
        output = process.read()
        process.close()
        if appid not in output:
            # 应用不在前台，运行应用
            print("游戏不在前台，正在启动")
            os.popen(f'{adb_path} -s {device_id} shell monkey -p {appid} -c android.intent.category.LAUNCHER 1')
            time.sleep(8)
        else:
            # 处理输出
            print('应用已在前台')
    except Exception as e:
        print(f'Error: {e}')
    

def where_am_i():
    is_game_on()
    screen = cv2.imread(api.get_screen_shot())
    # print(f'screen shape: {screen.shape}')
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_imgs = {
        'title': {'img': cv2.imread('img/title.png', cv2.IMREAD_GRAYSCALE), 'pos': (390, 240, 500, 220)},
        'policy': {'img': cv2.imread('img/agree.png', cv2.IMREAD_GRAYSCALE), 'pos': (600, 430, 200, 100)},
        'update': {'img': cv2.imread('img/download.png', cv2.IMREAD_GRAYSCALE), 'pos': (750, 400, 200, 50)},
        'login': {'img': cv2.imread('img/login.png', cv2.IMREAD_GRAYSCALE), 'pos': (590, 510, 200, 50)},
        'menu': {'img': cv2.imread('img/menu0.png', cv2.IMREAD_GRAYSCALE), 'pos': (48,506, 90, 90)},
        'nothome': {'img': cv2.imread('img/home.png', cv2.IMREAD_GRAYSCALE), 'pos': (120,25, 50, 50)},
        'notmenu': {'img': cv2.imread('img/back.png', cv2.IMREAD_GRAYSCALE), 'pos': (25,25, 50, 50)},
        'notmenu2': {'img': cv2.imread('img/back2.png', cv2.IMREAD_GRAYSCALE), 'pos': (25,25, 50, 50)},
    }

    # 使用cv2.matchTemplate函数和循环判断多个图像中的某一个是否在另一张图像中，并返回匹配到的图像的名称
    max_val = 0
    max_template_name = ''
    for template_name, template_info in template_imgs.items():
        x, y, w, h = template_info['pos']
        template_img = template_info['img']
        screen_gray_cropped = screen_gray[y:y+h, x:x+w]
        #print(f'screen_gray_cropped shape: {screen_gray_cropped.shape}')
        #print(f'template_img shape: {template_img.shape}')
        # 对图像和模板进行归一化
        #img_norm = cv2.normalize(screen_gray_cropped, None, 0, 255, cv2.NORM_MINMAX)
        #template_norm = cv2.normalize(template_img, None, 0, 255, cv2.NORM_MINMAX)
        # 对灰度图像进行直方图均衡化
        #img_eq = cv2.equalizeHist(screen_gray_cropped)
        #template_eq = cv2.equalizeHist(template_img)
        # 使用cv2.matchTemplate函数进行模板匹配
        result = cv2.matchTemplate(screen_gray_cropped, template_img, cv2.TM_CCOEFF_NORMED)
        if cv2.minMaxLoc(result)[1] > max_val:
            max_val = cv2.minMaxLoc(result)[1]
            max_template_name = template_name
            # 获取匹配结果矩阵中最大值的位置
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            # 获取模板图像的宽度和高度
            tw, th = template_img.shape[::-1]
            # 在匹配到的目标上画一个矩形框
            cv2.rectangle(screen, (x + max_loc[0], y + max_loc[1]), (x + max_loc[0] + tw, y + max_loc[1] + th), (0, 0, 255), 2)

    if max_val < 0.6:
        print('未匹配到任何模板图像')
        print(max_val,max_template_name)
        return None
    else:
        print(f'匹配到了{max_template_name}')
        # 将结果保存到cache/result.png文件中
        cv2.imwrite('cache/result.png', screen)
        return max_template_name

def login():
    api.touch(635,248)
    time.sleep(0.5)