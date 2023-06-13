import os
import json
import cv2
import numpy as np 
import paddleocr
from PIL import Image

with open('config.json', 'r') as f:
    config = json.load(f)
adb_path = config['adb_path']
device_id = config['device_id'] 
def get_screen_shot():
    os.system(f'{adb_path} -s {device_id} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def is_img_on(screen, template):
    result = cv2.matchTemplate(template, screen, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6  # 阈值
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
        print('匹配度过低'+ str(result))
        return None

def corp_ocr(x, y, w, h):
    """
    识别指定区域的文字
    :param x: 指定区域左上角的横坐标
    :param y: 指定区域左上角的纵坐标
    :param w: 指定区域的宽度
    :param h: 指定区域的高度
    """
    # 初始化PaddleOCR
    ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='ch')
    screen = cv2.imread(get_screen_shot())
    screen_corped = screen[y:y+h, x:x+w]
    result = ocr.ocr(screen_corped)
    # 遍历识别结果，获取每个词的文字
    print(result)
    text = ''
    for line in result:
        for word in line:
            if isinstance(word[1], str) and word[1].strip():
                text += word[1].strip()
    print(text)
    return text


def corp_ocr_with_coords(x, y, w, h):
    """
    识别指定区域的文字，并返回每个词及其在原图中的坐标
    :param x: 指定区域左上角的横坐标
    :param y: 指定区域左上角的纵坐标
    :param w: 指定区域的宽度
    :param h: 指定区域的高度
    :return words: 每个词的文字
    :return centers: 每个词的中心坐标
    """
    # 初始化PaddleOCR
    ocr = paddleocr(use_angle_cls=True, lang='ch')
    screen = paddleocr.read_image(get_screen_shot())
    screen_corped = screen[y:y+h, x:x+w]
    result = ocr.ocr(screen_corped)
    # 遍历识别结果，获取每个词的文字和中心坐标
    words = []
    centers = []
    for line in result:
        for word in line:
            if word[1].strip():
                left, top, right, bottom = word[0]
                center_x = left + (right - left) / 2
                center_y = top + (bottom - top) / 2
                words.append(word[1])
                centers.append((center_x + x, center_y + y))
    print(words)
    print(centers)
    return words, centers


def recoText(image, target):
    """
    识别字符并返回所识别的字符及它们的坐标
    :param image: 需要识别的图片路径
    :param target: 需要查找的目标文字
    :return left: 目标文字所在单词的左上角的横坐标
    :return top: 目标文字所在单词的左上角的纵坐标
    """
    with Image(image) as img:
        # 进行文字识别并返回识别结果和文字所在位置
        result = pytesseract.image_to_data(img, lang='chi_sim', output_type=Output.DICT)
        #print(result['text'])
        try:
            # 查找目标文字在识别结果中的位置
            index = result['text'].index(target)
            # 获取目标文字所在单词的位置信息
            left = result['left'][index]
            top = result['top'][index]
            return left, top
        except ValueError:
            print('未找到目标文字')
            return None, None
        

#adb相关
def touch(x,y):
    os.system(f'{adb_path} -s {device_id} shell input tap {x} {y}')

def swipe(x1,y1,x2,y2):
    os.system(f'{adb_path} -s {device_id} shell input swipe {x1} {y1} {x2} {y2}')

