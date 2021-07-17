import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

#参数
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

def get_roi_hsv(img):
    cv2.imshow('img', img)
    while(True):
        rect = cv2.selectROI('img', img, True, False)
        (x, y, w, h) = rect
        imCrop = img[y : y+h, x:x+w]

        img_hsv = cv2.cvtColor(imCrop, cv2.COLOR_BGR2HSV)

        hsvColor = (('h','r'), ('s', 'g'), ('v', 'b'))
        
        plt.title('hsv')
        for cidx, (label, color) in enumerate(hsvColor):
            cHist = cv2.calcHist([img_hsv], [cidx], None, [255], [0,255])
            plt.plot(cHist, color=color, label=label)

        plt.show()
        key = cv2.waitKey(0)
        if key == ord('q') or key == 27:
            break  

if __name__ == '__main__':
    img = cv2.imread(sys.argv[1])
    get_roi_hsv(img)

    cv2.destroyAllWindows()