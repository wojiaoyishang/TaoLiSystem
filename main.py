# 负责逻辑引导
import gc
import time
import sys
import uio

from mpython import *
from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

# 清理一下掌控板启动完毕之后的内存冗余
gc.collect()
print("可用总运存大小:", gc.mem_free())

# 导入模块函数
def importModule(name):
    exec("import " + name + " as pikachu_import_module")
    return pikachu_import_module

utils.importModule = importModule

# 全部页面模块
pages = ["TaoLiSystem.page.setting", "TaoLiSystem.page.home", "TaoLiSystem.page.plugin"]
page_id = 1  # 当前页面

# 当前页面编号
wait_close = False  # 是否准备关闭

# 此模块加载的模块，结束后释放
imported_not_modules = list(sys.modules.keys())

# 此刻的模块
imported_page = utils.importModule(pages[page_id])

def close_module():
    global page_id, imported_page, imported_not_modules
    
    print("释放页面前运存大小:", gc.mem_free())
    
    oled.fill(0)
    sysgui.draw_string_center("Loading......", 24)
    oled.show()
    
    imported_page.close()
    
    for m in list(sys.modules.keys()):
        if m not in imported_not_modules:
            print("* 删除多加载的模块:" + m)
            del sys.modules[m]
 
    gc.collect()

    print("释放页面后运存大小:", gc.mem_free())

def button_a_callback(_):
    global page_id, wait_close
    
    page_id = max(0, page_id - 1)
    
    print("* 即将加载页面:", pages[page_id])
    wait_close = True
    
def button_b_callback(_):
    global page_id, page, wait_close
    
    page_id = min(len(pages) - 1, page_id + 1)
    
    print("* 即将加载页面:", pages[page_id])
    wait_close = True
    

# 初始化设置
sysgui.tipBox("系统正在初始化......", 0)
# 连接 WIFI
if configData.read("system", "autoConnectWIFI") == "1":
    utils.enableWIFI()
    global_var['wifi'].sta.connect(configData.read("system", "autoConnectWIFI_ssid"),
                                          configData.read("system", "autoConnectWIFI_password"))
    
    time_ = time.time()
    while global_var['wifi'].sta.status() == 1001:
        if time.time() - time_ >= 10:
            break
        sysgui.tipBox("连接WIFI中(%ds)......" % int(time.time() - time_), 0)
    
    if time.time() - time_ >= 10:
        sysgui.tipBox("连接超时！", 1)
    else:
        message = {1000: "未连接", 1001: "正在连接", 202: "密码错误", 201: "接入点没有回复",
                   1010: "WIFI连接成功", 203: "方式请求错误", 200: "连接超时", 204: "握手超时"}[global_var['wifi'].sta.status()]
        
        sysgui.tipBox(message, 1)

# 同步时间
if "wifi" in global_var and global_var.get("wifi").sta.isconnected() and configData.read("system", "autoSyncTime") == "1":
    sysgui.tipBox("同步时间中......", 0)
    if utils.syncTime():
        sysgui.tipBox("同步时间成功！", 0)
    else:
        sysgui.tipBox("同步时间失败......", 0)
    
button_a.event_pressed = button_a_callback
button_b.event_pressed = button_b_callback

print("加载完毕运存大小:", gc.mem_free())

while True:
    try:
        if wait_close:
            button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 暂时禁用
            wait_close = False
            close_module()  # 释放页面
            button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
            imported_page = utils.importModule(pages[page_id])
            continue
        
        imported_page.show() 
            
    except KeyboardInterrupt as e:
        print("-" * 30)
        buffer = uio.StringIO()
        sys.print_exception(e, buffer)
        traceback_str = buffer.getvalue()
        buffer.close()
        print(traceback_str, end="")
        print("* 调试中断，程序正在退出......")
        break
    except BaseException as e:
        print("-" * 30)
        buffer = uio.StringIO()
        sys.print_exception(e, buffer)
        traceback_str = buffer.getvalue()
        buffer.close()
        
        print("* 程序运行时抛出了一个错误: ")
        print(traceback_str, end="")
        
        # 对一些已知错误标记
        if traceback_str.find("ValueError") != -1 and traceback_str.find("print_from_bin_by_pos") != -1:
            print("* 此错误由意外关闭bin文件打开文件对象导致。")
            
        print("-" * 30)
        
    
    



