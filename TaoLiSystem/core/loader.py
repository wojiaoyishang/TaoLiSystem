# 负责逻辑引导
import sys
import time

from mpython import *
from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

imported_not_modules = list(sys.modules.keys())  # 此模块加载的模块，结束后释放

# ==========================页面模块配置加载开始==========================
pages = []

pages.append("TaoLiSystem.page.setting")
for _ in __import__('json').loads(configData.read('system', 'homePages', '["default"]')):
    pages.append("TaoLiSystem.page.home." + _)
pages.append("TaoLiSystem.page.plugin")

page_id = int(configData.read('system', 'page_id', '1'))  # 当前页面

wait_close = False  # 是否准备关闭
bootconfig = {}  # 注意这里一段只是为了提醒末尾还有一句 bootconfig 配置读取
# ==========================页面模块配置加载结束==========================

def load_plugin():
    """
    减少代码复用，启动时调用插件函数
    """
    clean()
    sysgui.tipBox("加载插件中......", 0)
    print("插件可用运存：", utils.gc_collect())
    utils.importModule("TaoLiSystem.plugins." + bootconfig.get("module"))
    import machine
    machine.reset()
    

def before_init():
    """
    系统初始化之前
    """
    # 初始化设置
    sysgui.tipBox("系统正在初始化......", 0)
    # 清理一下掌控板启动完毕之后的内存冗余
    print("可用总运存大小:", utils.gc_collect())
    if bootconfig.get("mode") == "pluginrun" and bootconfig.get("priority") == 0:  # 初始化前加载插件
        load_plugin()

def after_init():
    """
    系统初始化之后
    """
    if bootconfig.get("mode") == "pluginrun" and bootconfig.get("priority") == 1:  # 初始化前加载插件
        load_plugin()
    
    # 绑定按钮事件
    button_a.event_pressed, button_b.event_pressed = button_a_callback, button_b_callback
  
    print("加载完毕运存大小:", utils.gc_collect())

def init():
    """
    系统初始化
    """
    # 调整屏幕亮度
    oled.contrast(int(configData.read("system", "ScreenContrast", "255")))
    # 连接 WIFI
    if configData.read("system", "autoConnectWIFI") == "1":
        utils.enableWIFI()
        wifi().sta.connect(configData.read("system", "autoConnectWIFI_ssid"),
                                              configData.read("system", "autoConnectWIFI_password"))
        
        time_ = time.time()
        while wifi().sta.status() == 1001:
            if time.time() - time_ >= 10:
                break
            sysgui.tipBox("连接WIFI中(%ds)......" % int(time.time() - time_), 0)
        
        if time.time() - time_ >= 10:
            sysgui.tipBox("连接超时！", 1)
        else:
            message = {1000: "未连接", 1001: "正在连接", 202: "密码错误", 201: "接入点没有回复",
                       1010: "WIFI连接成功", 203: "方式请求错误", 200: "连接超时", 204: "握手超时"}[wifi().sta.status()]
            
            sysgui.tipBox(message, 1)

        # 同步时间
        if utils.isConnectWIFI() and configData.read("system", "autoSyncTime") == "1":
            sysgui.tipBox("同步时间中......", 0)
            if utils.syncTime():
                sysgui.tipBox("同步时间成功！", 0)
            else:
                sysgui.tipBox("同步时间失败......", 0)

def read_bootconfig():
    """
    读取 bootconfig
    """
    try:
        import os
        import json
        with open("bootconfig", "r") as f:
            bootconfig = json.load(f)
        if not bootconfig.get("keep", False):
            os.remove("bootconfig")
        del os, json
        return bootconfig
    except:
        return {}

def clean():
    """
    删除初始化之后的所有内容
    """
    global init, read_bootconfig, load_plugin, before_init, after_init
    del init, read_bootconfig, load_plugin, before_init, after_init
    
def button_a_callback(_):
    global page_id, wait_close
    
    if not wait_close:  # 还没加载完毕时不可以切换
        page_id = max(0, page_id - 1)
        print("* 即将加载页面:", pages[page_id])
        wait_close = True
    
def button_b_callback(_):
    global page_id, page, wait_close
    
    if not wait_close:  # 还没加载完毕时不可以切换
        page_id = min(len(pages) - 1, page_id + 1)
        print("* 即将加载页面:", pages[page_id])
        wait_close = True
    
def close_module():
    global wait_close, imported_page, imported_not_modules
    print("释放页面前运存大小:", utils.gc_collect())
    
    if wait_close:
        oled.fill(0)
        sysgui.draw_string_center("Loading......", 24)
        oled.show()
        
        imported_page.close()
        
        utils.compare_and_clean_modules(imported_not_modules, [])

        print("释放页面后运存大小:", utils.gc_collect())
    
def main_loop():
    """
    系统主循环
    """
    global pages, page_id, imported_page, wait_close
    
    imported_page = utils.importModule(pages[page_id])  # 系统最初的模块
    
    while True:
        try:
            if wait_close:
                button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 暂时禁用
                button_a.event_pressed, button_b.event_pressed = None, None
                close_module()  # 释放页面
                button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
                imported_page = utils.importModule(pages[page_id])
                wait_close = False
                continue
            
            imported_page.show() 
                
        except KeyboardInterrupt as e:
            print("-" * 30)
            buffer = __import__('uio').StringIO()
            sys.print_exception(e, buffer)
            traceback_str = buffer.getvalue()
            buffer.close()
            print(traceback_str, end="")
            print("* 调试中断，程序正在退出......")
            break
        except BaseException as e:
            print("-" * 30)
            buffer = __import__('uio').StringIO()
            sys.print_exception(e, buffer)
            traceback_str = buffer.getvalue()
            buffer.close()
            
            print("* 程序运行时抛出了一个错误: ")
            print(traceback_str, end="")
            
            # 对一些已知错误标记
            if traceback_str.find("ValueError") != -1 and traceback_str.find("print_from_bin_by_pos") != -1:
                print("* 此错误由意外关闭bin文件打开文件对象导致。")
                
            print("-" * 30)
        
    
bootconfig = read_bootconfig()