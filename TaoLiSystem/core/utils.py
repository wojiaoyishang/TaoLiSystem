import os
import bluetooth

from mpython import *
from TaoLiSystem.core import sysgui
from TaoLiSystem.core.config import *

importModule = None  # main.py 会给赋值

def convert_ms_to_hms(milliseconds):
    """
    转化毫秒到时分秒
    """
    # 将毫秒转化为秒
    total_seconds = milliseconds // 1000
    remaining_ms = milliseconds % 1000
    # 计算时、分、秒
    hours = total_seconds // 3600
    total_seconds %= 3600
    minutes = total_seconds // 60
    total_seconds %= 60
    seconds = total_seconds

    return int(hours), int(minutes), int(seconds), int(remaining_ms)

def isEnableWIFI():
    return 'wifi' in global_var and global_var['wifi'].sta.isconnected()

def enableWIFI():
    global_var['wifi'] = wifi()
    global_var['wifi'].sta.active(True)

def disableWIFI():
    if isEnableWIFI():
        global_var['wifi'].sta.disconnect()
        global_var['wifi'].sta.active(False)
        del global_var['wifi']

def isEnableBluetooth():
    return 'bluetooth_BLE' in global_var

def enableBluetooth():
    global_var['bluetooth_BLE'] = bluetooth.BLE()
    global_var['bluetooth_BLE'].active(True)

def disableBluetooth():
    if isEnableBluetooth():
        global_var['bluetooth_BLE'].active(False)
        del global_var['bluetooth_BLE']
    else:
        bluetooth.BLE().active(False)

def syncTime():
    ntptime = __import__("ntptime")  # 动态导入
    try:
        ntptime.settime(timezone=8, server = 'ntp1.aliyun.com')
        return True
    except:
        return False

def delete_folder(folder):
    """文件夹，包含有文件的文件夹"""
    if folder[-1] != "/":
        folder += "/"
    for file_info in os.ilistdir(folder):
        if file_info[1] == 16384:  # 是文件夹
            delete_folder(folder + "/" + file_info[0])
            os.rmdir(folder + "/" + file_info[0])
        else:
            print("* 删除文件 %s" % (folder + "/" + file_info[0]))
            os.remove(folder + "/" + file_info[0])

def debug(g, l, v=None):
    """变量监控与调试工具 使用方法 utils.debug(globals(), locals())"""
    HELP_TEXT = "g 变量是全局参数，l 变量是局部参数，v 变量是额外用户提供的变量\n" + \
                "help -- 查看帮助\n" + \
                "return [参数] -- 退出调试，返回参数\n" + \
                "var [变量名] -- 查看变量\n" + \
                "exe [表达式] -- 执行表达式"

    print("=" * 5 + "Debug Mode" + "=" * 5)
    print(HELP_TEXT)

    while True:
        user = input("Debug >> ").split(" ")
        if user[0] == "return":
            if len(user) == 1:
                return
            elif len(user) == 2:
                try:
                    return eval(user[1], globals(), locals())
                except BaseException as e:
                    print(str(e))
        elif user[0] == "help":
            print(HELP_TEXT)
        elif user[0] == "var":
            if len(user) == 1:
                print("全局变量:", g.keys())
                print("局部变量:", l.keys())
            elif len(user) == 2:
                if user[1] in g:
                    print("全局中%s的值:" % user[0], g[user[1]])
                if user[1] in l:
                    print("局部中%s的值:" % user[0], l[user[1]])
            else:
                print("命令输入错误。")
        elif user[0] == "exe":
            cmd = " ".join(user[1:])
            print("exec返回结果:", exec(cmd, globals(), locals()))
