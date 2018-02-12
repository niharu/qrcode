# -*- coding: utf-8 -*-

import copy
from PIL import Image, ImageDraw

def create_qr_data():
    return [32,65,205,69,41,220,46,128,236,42,159,74,221,244,169,239,150,138,70,237,85,224,96,74,219,61]

def write_default_pattern(data_map):
    tmp_map = copy.deepcopy(data_map)

    # write timing pattern
    for i in range(0, len(data_map[0])):
        if i % 2 == 0:
            tmp_map[i][7-1] = 1
            tmp_map[7-1][i] = 1
        else:
            tmp_map[i][7-1] = 0
            tmp_map[7-1][i] = 0

    tmp_map[13][8] = 1

    # write 3 corner white
    tmp_map = write_white_corner(tmp_map, 8)

    # write 3 pos pattern
    tmp_map = write_pos_pattern(tmp_map, 0, 0, 7)
    tmp_map = write_pos_pattern(tmp_map, len(data_map[0])-7, 0, 7)
    tmp_map = write_pos_pattern(tmp_map, 0, len(data_map[0])-7, 7)

    return tmp_map

def write_white_corner(data_map, side_len):
    tmp_map = copy.deepcopy(data_map)
    tmp_map = write_square(tmp_map, 0, 0, side_len, 0)
    tmp_map = write_square(tmp_map, len(data_map[0])-side_len, 0, side_len, 0)
    tmp_map = write_square(tmp_map, 0, len(data_map[0])-side_len, side_len, 0)
    return tmp_map

def write_pos_pattern(data_map, pos_x, pos_y, side_len):
    tmp_map2 = copy.deepcopy(data_map)
    # black_square
    tmp_map2 = write_square(tmp_map2, pos_x, pos_y, side_len, 1)
    # white_square
    tmp_map2 = write_square(tmp_map2, pos_x+1, pos_y+1, side_len-2, 0)
    # black_square
    tmp_map2 = write_square(tmp_map2, pos_x+2, pos_y+2, side_len-4, 1)
    return tmp_map2

def write_square(data_map, pos_x, pos_y, side_len, bit):
    tmp_map = copy.deepcopy(data_map)
    
    for i in range(pos_y, pos_y+side_len):
        for j in range(pos_x, pos_x+side_len):
            tmp_map[i][j] = bit

    return tmp_map
    
def draw_data_map(data_map):
    im = Image.new('RGB', (230, 230), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(0, len(data_map[0])):
        for j in range(0, len(data_map[i])):
            if data_map[i][j] == 1:
                draw.rectangle((j*10+10,i*10+10,j*10+20,i*10+20), fill=(0,0,0))
            elif data_map[i][j] == 2:
                draw.rectangle((j*10+10,i*10+10,j*10+20,i*10+20), fill=(255,255,0))

    im.save('pillow_imagedraw.jpg', quality=95)

def get_info_format():
    return [0,0,0,0,1,0,1,1,1,0,0,1,1,0,0]

def write_info_format(data_map, info_format):
    tmp_map = copy.deepcopy(data_map)
    first_half = info_format[0:8]
    second_half = info_format[8:15]

    for i in range(0,len(first_half)):
        tmp_map[8][len(data_map[0])-1-i] = first_half[i]

    k = 0
    for info in first_half:
        if tmp_map[k][8] != 2:
            k += 1
        tmp_map[k][8] = info
        k += 1

    k = 0
    for info in second_half:
        if tmp_map[8][7-k] != 2:
            k += 1
        tmp_map[8][7-k] = info
        k += 1

    for i in range(0,len(second_half)):
        tmp_map[len(data_map[0])-7+i][8] = second_half[i]

    return tmp_map

def write_qr_data(data_map, qr_info):
    print("len(qr_info)",len(qr_info))
    tmp_map = copy.deepcopy(data_map)
    i = len(data_map[0]) - 1
    j = len(data_map[0]) - 1
    k = 0
    cnt = 0
    v = -1 # upper
    while k < 208:
        print("cnt:",cnt)
        cnt += 1
        print(i,j)
        if i < 0 :
            i += 1
            j -= 2
            v *= -1
            continue
        elif i >= len(data_map[0]):
            i -= 1
            j -= 2
            v *= -1
            continue

        if tmp_map[i][j] == 2:
            tmp_map[i][j] = int(qr_info[k]) + 3
            k += 1

        if j % 2 == 0: # upper or down
            j -= 1
        else:
            # upper
            j += 1
            i += v


    return tmp_map

def mask_map(data_map):
    tmp_map = copy.deepcopy(data_map)
    for i in range(0,21):
        for j in range(0,21):
            if tmp_map[i][j] == 3 and (i+j) % 3 == 0:
                print(i,j)
                tmp_map[i][j] = 1
            elif tmp_map[i][j] == 4 and (i+j) % 3 == 0:
                print(i,j)
                tmp_map[i][j] = 0
            elif tmp_map[i][j] > 2:
                tmp_map[i][j] = tmp_map[i][j] - 3
    return tmp_map

if __name__ == "__main__":
    qr_data = create_qr_data()
    data_map = [[2 for i in range(0,21)] for j in range(0,21)]

    data_str = ''
    for data in qr_data:
        data_str += str(bin(data)[2:]).zfill(8)
    print(data_str)
    print("data_str len:", len(data_str))

    result_map = write_default_pattern(data_map)

    result_map = write_info_format(result_map, get_info_format())

    cnt = 0
    for m in result_map:
        for n in m:
            if n == 2:
                cnt += 1
    print("cnt",cnt)

    result_map = write_qr_data(result_map, data_str)

    result_map = mask_map(result_map)

    draw_data_map(result_map)

    for i in range(0,21):
        for j in range(0,21):
            if j == 20:
                print(result_map[i][j])
            else:
                print(str(result_map[i][j]), end=" ")

