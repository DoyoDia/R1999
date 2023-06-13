import os
import cv2

# 遍历img文件夹下后缀为.png的所有图像，并将它们转换为灰度图像
for filename in os.listdir('img/origin'):
    if filename.endswith('.png'):
        img = cv2.imread(f'img/origin/{filename}')
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f'img/{filename}', img_gray)