import numpy as np
import cv2


def loc(x, x_min, w):
    # location
    # 左边或者右边有一块黑色无效的区域，剪掉;
    if x < x_min + 0.8*w:
        return 0
    elif x < x_min + 1.8*w:
        return 1
    elif x < x_min + 2.8*w:
        return 2


def analyse_color(all_rects, white, red, orange, yellow, green, blue):
    w_aver = 0
    h_aver = 0
    # width average
    x_min = all_rects[0][0]
    y_min = all_rects[0][1]
    color_map = [['?', '?', '?'],
                 ['?', '?', '?'],
                 ['?', '?', '?']]

    # 确定 w_aver h_aver x_min y_min
    for each in all_rects:
        w_aver += each[2]
        h_aver += each[3]
        if each[0] < x_min:
            x_min = each[0]
        if each[1] < y_min:
            y_min = each[1]
    w_aver /= len(all_rects)
    h_aver /= len(all_rects)

    for rect in white:
        # rect:矩形
        if loc(rect[1], y_min, h_aver) != None and loc(rect[0], x_min, w_aver) != None:
            color_map[loc(rect[1], y_min, h_aver)][loc(
                rect[0], x_min, w_aver)] = 'W'
    for rect in red:
        if loc(rect[1], y_min, h_aver) != None and loc(rect[0], x_min, w_aver) != None:
            color_map[loc(rect[1], y_min, h_aver)][loc(
                rect[0], x_min, w_aver)] = 'R'
    for rect in orange:
        if loc(rect[1], y_min, h_aver) != None and loc(rect[0], x_min, w_aver) != None:
            color_map[loc(rect[1], y_min, h_aver)][loc(
                rect[0], x_min, w_aver)] = 'O'
    for rect in yellow:
        if loc(rect[1], y_min, h_aver) != None and loc(rect[0], x_min, w_aver) != None:
            color_map[loc(rect[1], y_min, h_aver)][loc(
                rect[0], x_min, w_aver)] = 'Y'
    for rect in green:
        if loc(rect[1], y_min, h_aver) != None and loc(rect[0], x_min, w_aver) != None:
            color_map[loc(rect[1], y_min, h_aver)][loc(
                rect[0], x_min, w_aver)] = 'G'
    for rect in blue:
        if loc(rect[1], y_min, h_aver) != None and loc(rect[0], x_min, w_aver) != None:
            color_map[loc(rect[1], y_min, h_aver)][loc(
                rect[0], x_min, w_aver)] = 'B'

    str_pos = ''
    for row in color_map:
        for item in row:
            str_pos += item

    return color_map, str_pos
