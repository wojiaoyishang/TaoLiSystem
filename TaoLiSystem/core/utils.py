import os
import gc
import sys
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
    return wifi().sta.active()

def isConnectWIFI():
    return wifi().sta.isconnected()

def enableWIFI():
    wifi().sta.active(True)

def disableWIFI():
    if isEnableWIFI():
        wifi().sta.disconnect()
        wifi().sta.active(False)

def isEnableBluetooth():
    import bluetooth
    return bluetooth.BLE().active()

def enableBluetooth():
    global global_var
    ble = bluetooth.BLE()
    result = ble.active(True)
    if result:
        global_var['bluetooth_BLE'] = ble
    return result

def disableBluetooth():
    global global_var
    if 'bluetooth_BLE' in global_var:
        global_var['bluetooth_BLE'].active(False)
        del global_var['bluetooth_BLE']

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

def gc_collect():
    """反复清理"""
    m = gc.mem_free()
    n = 3
    gc.collect()
    while n > 0:
        if m == gc.mem_free():
            gc.collect()
            n -= 1
        else:
            m = gc.mem_free()
            gc.collect()
            n = 3
    return m

def compare_and_clean_modules(imported_not_modules, KEEP_MODULES=[]):
    """比较而后清理多于的模块"""
    for m in list(sys.modules.keys()):
        if m not in imported_not_modules and m not in KEEP_MODULES:
            i = 0
            for l in dir(sys.modules[m]):
                try:
                    setattr(sys.modules[m], l, None)
                    i += 1
                    # print("* 删除多加载模块对象:%s %s" % (m, l))
                except AttributeError:
                    continue
            print("* 删除多加载的模块:%s (对象个数:%d)" % (m, i))
            del sys.modules[m]
 
    gc_collect()

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

