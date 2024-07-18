# 简单打包自动下载到掌控板，运行使用命令行操作，完善了 Micropython 中批量下载文件的功能。 By Yishang
import os
import pyboard

# 代码来自 sysgui
display_cmd = r"""from mpython import *
def get_character_width(s):
    width = 0
    for character in s:
        if character == "" or character is None:
            return 0
        character_data = oled.f.GetCharacterData(character)
        if character_data is None:
            return None
        width += ustruct.unpack('HH', character_data[:4])[0] + 1 
    return width - 1
def draw_rect_empty(x1, y1, x2, y2, function=None, no_fill=False):
    if not no_fill:
        oled.fill_rect(x1 + 1, y1 + 1, x2 - 2, y2 - 2, 0)
    if function:
        function()
    oled.rect(x1, y1, x2, y2, 1)   
def draw_string_center(text, y, mode=TextMode.normal, ex=False):
    i = 0
    text = text.split("\n")
    for t in text:
        text_width = get_character_width(t)
        if not ex:
            oled.DispChar(t, int(128 / 2 - text_width / 2) + i * 16, y, mode)
        else:
            oled.DispChar(t, int(128 / 2 - text_width / 2), int(64 / 2 - 16 * len(text) / 2) - y + i * 16, mode)
        i += 1
def tipBox(content, t=3):
    draw_rect_empty(1, 1, 126, 62, lambda : draw_string_center(content, 0, ex=True))
"""


def fs_put_batch_callback(file, written, src_size):
    print("正在传输文件 " + file + "...... 进度：", str(round(written / src_size * 100, 2)) + "%")


def fs_put_batch_download(pyb, path, d, chunk_size, progress_callback, ignore_files, delete_py=False):  # 结尾没有分割符号
    if os.path.isdir(path):
        try:
            if d not in ("", "/"):
                pyb.fs_mkdir(d)
        except:
            pass
        for file in os.listdir(path):
            fs_put_batch_download(pyb, path + "/" + file, d + "/" + file, chunk_size,
                                  progress_callback=progress_callback, ignore_files=ignore_files, delete_py=delete_py)
    else:
        if d not in ignore_files:
            pyb.exec(display_cmd)
            if d[d.rfind('.'):] == ".mpy":
                py_file_path = d[:d.rfind('.')] + ".py"
                if delete_py and pyb.fs_exists(py_file_path):
                    print(f"正在删除掌控板上的 {py_file_path} ......")
                    pyb.exec(fr"oled.fill(0);tipBox('正在删除 \n{py_file_path[py_file_path.rfind('/') + 1:]}');oled.show()")
                    pyb.fs_rm(py_file_path)
            pyb.exec(fr"oled.fill(0);tipBox('正在传输 \n{d[d.rfind('/') + 1:]}');oled.show()")
            pyb.fs_put(path, d, chunk_size=chunk_size, progress_callback=lambda x, y: fs_put_batch_callback(d, x, y))


def fs_put_batch(pyb, filelist, dest, chunk_size=256, progress_callback=None, ignore_files=[], delete_py=False):
    """
    批量复制文件，注意：直接覆盖原文件

    :param pyb: pyb
    :param filelist: 文件列表
    :param dest: 目标地址
    :param chunk_size: 每次传输大小
    :param progress_callback: 传输回调
    :param ignore_files: 不复制的文件
    :param delete_py: 删除未编译文件。
    :return:
    """
    if isinstance(filelist, str):
        filelist = [filelist]

    if progress_callback is None:
        progress_callback = fs_put_batch_callback

    for file in filelist:
        fs_put_batch_download(pyb, file, dest, chunk_size, progress_callback, ignore_files=ignore_files, delete_py=delete_py)

    pyb.exec(fr"oled.fill(0);tipBox('全部文件传输完毕。');oled.show()")


def fs_rm_batch(pyb, path, progress_callback=None):
    """
    批量删除文件

    :param pyb: pyb
    :param path: 文件路径
    :param progress_callback: 回调
    """
    if progress_callback is None:
        def progress_callback(path):
            print(f"正在删除  Micropython 中的 {path} ......")

    if pyb.fs_stat(path).st_mode == 16384:  # 是文件夹
        for file in pyb.fs_listdir(path):
            fs_rm_batch(pyb, path + "/" + file.name, progress_callback=progress_callback)
        pyb.fs_rmdir(path)
    else:
        progress_callback(path)
        pyb.exec(display_cmd)
        pyb.exec(fr"oled.fill(0);tipBox('正在删除 \n{path[path.rfind('/') + 1:]}');oled.show()")
        pyb.fs_rm(path)
