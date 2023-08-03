# https://gitee.com/wojiaoyishang/new-mpython-bin-to-pricture

import gc
from mpython import *

# 该函数用于绘制一行图像
def _draw_line(x, y, t, image_width, image_height, point_count, c):
    """
    Args:
        x (int): 图像的起始 x 坐标
        y (int): 图像的起始 y 坐标
        t (int): 剩余需要绘制的点数
        image_width (int): 图像的宽度
        image_height (int): 图像的高度
        point_count (int): 已绘制的点数
        c (int): 当前绘制行的颜色，可以为0或1

    Returns:
        t (int): 更新后剩余需要绘制的点数
        image_height (int): 更新后的图像高度
        point_count (int): 更新后已绘制的点数
        c (int): 更新后的颜色值
    """
    # t表示该行的像素数，point_count记录已绘制的像素数，c是颜色
    while t > 0:
        if image_width - point_count <= t:
            # 当前行剩余像素足够绘制
            oled.line(x + point_count, y + image_height, x + point_count + image_width - point_count - 1, y + image_height, c)
            t -= image_width - point_count
            point_count = 0
            image_height += 1
        else:
            # 当前行剩余像素不足，只能绘制部分
            oled.line(x + point_count, y + image_height, x + point_count + t - 1, y + image_height, c)
            point_count += t
            t = 0

    # 颜色切换
    c = 1 - c

    return t, image_height, point_count, c


# 该函数从二进制文件中读取并打印图像
def print_from_bin(x, y, fp, target_image_name, buff_size=None, color_invert=False, draw_line_fun=_draw_line):
    """
    Args:
        x (int): 图像的起始 x 坐标
        y (int): 图像的起始 y 坐标
        fp (file): 需要读取的二进制文件
        target_image_name (str): 目标图像的名称
        buff_size (int, optional): 缓冲区大小。如果未指定，则为可用内存的 20%
        color_invert (bool, optional): 是否颠倒颜色，默认为False
        draw_line_fun (function, optional): 用于绘制图像的函数，默认为_draw_line

    Returns:
        image_width (int): 打印的图像宽度
        image_height (int): 打印的图像高度
    """
    target_image_name = target_image_name.encode('utf-8')

    buff = bytearray(buff_size if buff_size else int(gc.mem_free() * 0.2))  # 创建一个bytearray作为缓冲区
    buff_view = memoryview(buff)
    fp.seek(0)
    b = fp.readinto(buff_view)  # 读取数据到缓冲区
    b_offset = 0  # 设置读取缓冲区的位置偏移量
    temp = bytearray()
    empty_times = 0
    found, image_width, image_height = False, 0, 0
    point_count = 0
    c = 0 if not color_invert else 1  # 颜色设置

    while b:
        # 在buff中寻找图像数据
        if buff[b_offset] == 255:  # '\xff'
            if empty_times % 3 == 1 and temp == target_image_name:
                found = True
            elif found and empty_times % 3 == 2:
                image_width = int(temp.decode('utf-8'))
            elif found and empty_times % 3 == 0:
                break
            empty_times += 1
            temp = bytearray()
        else:
            if not found and empty_times % 3 == 1:
                temp.extend(buff[b_offset:b_offset+1])
            elif found and empty_times % 3 == 2:
                temp.extend(buff[b_offset:b_offset+1])
            elif found and empty_times % 3 == 0:
                t = int.from_bytes(buff[b_offset:b_offset+1], "big")
                t, image_height, point_count, c = draw_line_fun(x, y, t, image_width, image_height, point_count, c)

        b_offset += 1  # 移动到下一个字节

        if b_offset >= b:
            b = fp.readinto(buff_view)
            b_offset = 0  # 重置偏移量
    
    del buff, buff_view, temp
    gc.collect()
    return image_width, image_height


# 该函数用于获取二进制数据的位置
def get_bin_data_pos(fp, target_image_name, buff_size=None):
    """
    Args:
        fp (file): 需要读取的二进制文件
        target_image_name (str or list): 目标图像的名称，可以是单个图像名称或多个图像名称的列表
        buff_size (int, optional): 缓冲区大小。如果未指定，则为可用内存的 20%

    Returns:
        result (dict): 字典，包含找到的每个目标图像名称及其在二进制文件中的位置
    """
    result = {}

    if not isinstance(target_image_name, list):
        target_image_name = [target_image_name.encode('utf-8')]
    else:
        target_image_name = list(set(i.encode('utf-8') for i in target_image_name))

    buff_size = buff_size if buff_size else int(gc.mem_free() * 0.2)

    buff = bytearray(buff_size)  # 创建一个bytearray作为缓冲区
    buff_view = memoryview(buff)
    fp.seek(0)
    b = fp.readinto(buff_view)  # 读取数据到缓冲区
    b_offset = 0  # 设置读取缓冲区的位置偏移量
    temp = bytearray()
    empty_times = 0
    found, image_width = False, 0
    point_count = 0

    while b:
        if buff[b_offset] == 255:  # '\xff'
            if empty_times % 3 == 1 and temp in target_image_name:  # 图片名称
                found = True
                result[temp.decode('UTF-8')] = fp.tell() - b + b_offset - len(temp) - 1
            empty_times += 1
            temp = bytearray()
        else:
            if not found and empty_times % 3 == 1:  # 图片文件名读取
                temp.extend(buff[b_offset:b_offset+1])
            elif found and empty_times % 3 == 0:  # 找到数据段说明文件名与宽度已经找寻完毕
                found = False

        if len(result) == len(target_image_name):
            break

        b_offset += 1  # 移动到下一个字节

        if b_offset >= b:
            b = fp.readinto(buff_view)
            b_offset = 0  # 重置偏移量
    
    del buff, buff_view, temp
    gc.collect()
    return result


# 该函数根据二进制数据的位置打印图像
def print_from_bin_by_pos(x, y, fp, pos, buff_size=None, color_invert=False, draw_line_fun=_draw_line):
    """
    Args:
        x (int): 图像的起始 x 坐标
        y (int): 图像的起始 y 坐标
        fp (file): 需要读取的二进制文件
        pos (int): 目标图像在二进制文件中的位置
        buff_size (int, optional): 缓冲区大小。如果未指定，则为可用内存的 20%
        color_invert (bool, optional): 是否颠倒颜色，默认为False
        draw_line_fun (function, optional): 用于绘制图像的函数，默认为_draw_line

    Returns:
        image_width (int): 打印的图像宽度
        image_height (int): 打印的图像高度
    """
    image_height = 0
    point_count = 0
    c = 0 if not color_invert else 1  # 颜色设置

    buff_size = buff_size if buff_size else int(gc.mem_free() * 0.2)

    buff = bytearray(buff_size)  # 创建一个bytearray作为缓冲区
    b_offset = 0  # 设置读取缓冲区的位置偏移量
    if pos < 0:
        raise ValueError("pos is incorrect.")
    fp.seek(pos)
    buff_view = memoryview(buff)
    b = fp.readinto(buff_view)
    temp = bytearray()
    empty_times = 0
    found, image_width, image_height = False, 0, 0
    point_count = 0
    c = 0 if not color_invert else 1
    if buff[0] != 255:
        raise ValueError("pos is incorrect.")
    while b:
        if buff[b_offset] == 255:  # '\xff'
            if empty_times % 3 == 1:
                found = True
            elif found and empty_times % 3 == 2:
                image_width = int(temp.decode('utf-8'))
            elif found and empty_times % 3 == 0:
                break
            empty_times += 1
            temp = bytearray()
        else:
            if not found and empty_times % 3 == 1:
                temp.extend(buff[b_offset:b_offset+1])
            elif found and empty_times % 3 == 2:
                temp.extend(buff[b_offset:b_offset+1])
            elif found and empty_times % 3 == 0:
                t = int.from_bytes(buff[b_offset:b_offset+1], "big")
                t, image_height, point_count, c = draw_line_fun(x, y, t, image_width, image_height, point_count, c)

        b_offset += 1  # 移动到下一个字节

        if b_offset >= b:
            b = fp.readinto(buff_view)
            b_offset = 0  # 重置偏移量
            
    del buff, buff_view, temp
    gc.collect()
    return image_width, image_height



