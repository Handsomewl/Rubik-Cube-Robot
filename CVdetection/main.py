import numpy as np
import cv2
import sys
import time
#from matplotlib import pyplot as plt
#from skimage import morphology

import analyse
from color_feature import color_block_finder, draw_color_block_rect
import get_solution
import my_serial


#参数
bgx=180
bgy=50
white_lower=(0,0,90)
white_upper=(180,55,255)
red_1_lower=(0,55,40)
red_1_upper=(10,255,190)
red_2_lower=(135,55,40)
red_2_upper=(180,255,190)
orange_1_lower=(0,55,191)
orange_1_upper=(10,255,255)
orange_2_lower=(156,55,191)
orange_2_upper=(180,255,255)
orange_3_lower=(11,25,50)
orange_3_upper=(19,255,255)
yellow_lower=(20,55,55)
yellow_upper=(46,255,255)
green_lower=(47,55,40)
green_upper=(99,255,255)
blue_lower=(100,55,40)
blue_upper=(124,255,255)

def color_recognition(img, img_sort):
    '''
    识别  -> color_map, color_str
    img_sort: 0->前景提取 1->阈值+切片
    '''
    #长度阈值
    if img_sort == 0:
        min_l = min(img.shape[1]/10, img.shape[0]/10)
        max_l = min(img.shape[1]/4, img.shape[0]/4)
        #去除小区域
        img = remove_small_area(img)

    else:
        min_l = min(img.shape[1]/6, img.shape[0]/6)
        max_l = min(img.shape[1]/3, img.shape[0]/3)        

    # 前景提取：提取出魔方的大致区域，在魔方在图像中的占比大致为90%以上；

    # rects区域
    # 确定6种颜色对应的矩形区域；
    all_rects = []
    img_bin, white_rects = color_block_finder(img, [[white_lower, white_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, red_rects = color_block_finder(img, [[red_1_lower, red_1_upper], [red_2_lower, red_2_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, orange_rects = color_block_finder(img, [[orange_1_lower, orange_1_upper], [orange_2_lower, orange_2_upper], [orange_3_lower, orange_3_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, yellow_rects = color_block_finder(img, [[yellow_lower, yellow_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, green_rects = color_block_finder(img, [[green_lower, green_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, blue_rects = color_block_finder(img, [[blue_lower, blue_upper]], all_rects, min_l, max_l, min_l, max_l)

    #画图
    #把6种颜色区域的边框绘制在原图像上，可以确定是否找对了魔方区域；
    img_draw = img.copy()
    img_draw = draw_color_block_rect(img_draw, white_rects, (245,245,245))
    img_draw = draw_color_block_rect(img_draw, red_rects, (42,42,165))
    img_draw = draw_color_block_rect(img_draw, orange_rects, (0,140,255))
    img_draw = draw_color_block_rect(img_draw, yellow_rects, (0,255,255))
    img_draw = draw_color_block_rect(img_draw, green_rects, (0,255,0))
    img_draw = draw_color_block_rect(img_draw, blue_rects, (255,0,0))
    cv2.imshow('img_draw', img_draw)

    #分析
    return analyse.analyse_color(all_rects, white_rects, red_rects, orange_rects, yellow_rects, green_rects, blue_rects)
        

def get_video_rect(img):
    # 从摄像头获得一张图片；
    '''
    ->img_draw
    '''
    min_l = min(img.shape[1]/10, img.shape[0]/10)
    max_l = min(img.shape[1]/4, img.shape[0]/4)

    #rects区域
    all_rects = []
    img_bin, white_rects = color_block_finder(img, [[white_lower, white_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, red_rects = color_block_finder(img, [[red_1_lower, red_1_upper], [red_2_lower, red_2_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, orange_rects = color_block_finder(img, [[orange_1_lower, orange_1_upper], [orange_2_lower, orange_2_upper], [orange_3_lower, orange_3_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, yellow_rects = color_block_finder(img, [[yellow_lower, yellow_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, green_rects = color_block_finder(img, [[green_lower, green_upper]], all_rects, min_l, max_l, min_l, max_l)
    img_bin, blue_rects = color_block_finder(img, [[blue_lower, blue_upper]], all_rects, min_l, max_l, min_l, max_l)

    #画图
    img_draw = img.copy()
    img_draw = draw_color_block_rect(img_draw, white_rects, (245,245,245))
    img_draw = draw_color_block_rect(img_draw, red_rects, (42,42,165))
    img_draw = draw_color_block_rect(img_draw, orange_rects, (0,140,255))
    img_draw = draw_color_block_rect(img_draw, yellow_rects, (0,255,255))
    img_draw = draw_color_block_rect(img_draw, green_rects, (0,255,0))
    img_draw = draw_color_block_rect(img_draw, blue_rects, (255,0,0))
    
    return img_draw


if __name__ == '__main__':
    '''
    argv[1] 端口  例：python main.py com9
    拍摄时，空格确定，r撤回
    '''
    str_total = ''
    cap = cv2.VideoCapture(0)
    flag = True

    print('上 右 前 下 左 后\n红 黄 绿 橙 白 蓝')

    i = 0
    while(i < 6):
        #URFDLB 上右前下左后
        color_str = None
        while(flag):
            _, img = cap.read()
            #去除摄像头的黑边
            img = img[60:]
            img = img[:img.shape[0]-60]

            #显示摄像头
            img_rect = get_video_rect(img)
            cv2.rectangle(img_rect, (bgx, bgy), (img.shape[1]-bgx, img.shape[0]-bgy), (139,34,104), 3)
            text_dict = {0:'Up', 1:'Right', 2:'Front', 3:'Down', 4:'Left', 5:'Back'}
            cv2.putText(img_rect, text_dict[i], (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (139,34,104), 2)
            cv2.imshow('video', img_rect)

            key = cv2.waitKey(50)
            # key是键盘上输入；

            #确定
            if key == 32:
                #方案二：直接阈值识别，包含前景提取；
                img = img[bgy:img.shape[0]-bgy, bgx:img.shape[1]-bgx]
                color_map, color_str = color_recognition(img, 1)
                break

            #退出
            elif key == 27:
                flag = False
                
            #撤回
            elif key == ord('r'):
                str_total = ''.join(str_total.split()[:-1])
                i -= 1

        i += 1
        str_total = str_total + ' ' + color_str
        print(str_total)

        if i==6:
            try:
                _str_total = ''.join(str_total.split())
                _str_solution = get_solution.get_solution(_str_total)
            except:
                str_total = ''.join(str_total.split()[:-1])
                i -= 1

    cap.release()
    str_total = ''.join(str_total.split())

str_solution = get_solution.get_solution(str_total)

print(str_solution)

time.sleep(3)

start = cv2.waitKey(0)
while(start != 32):
    start = cv2.waitKey(0)

#发送
x=1 #发送次数
ser = my_serial.Ser(sys.argv[1])
ser.send_cmd(str_solution + '#')
print(x)
time.sleep(0.5)

flag = True
while(flag):
    if ser.get_in_waiting():
        print(ser.read(2))
        flag = False
    else:
        ser.send_cmd(str_solution+'#')
        x+=1
        print(x)
        time.sleep(0.5)

time.sleep(3)
print(ser.readall())

cv2.destroyAllWindows()
ser.close()