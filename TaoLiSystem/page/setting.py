# 设置页面的绘制
import time
import sys
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

from TaoLiSystem.page import settingFun

setting_id = 0  # 当前设置项
enter_time = 3  # 进入设置项倒计时

# 是否需要提示
tip1 = configData.read("system", "settingTipped") != "1"  # 设置选择页面
tip2 = configData.read("system", "itemSelectorTipped") != "1"  # 物品选择提示

# 绘制 GUI 所需的文件
gui_fp = open("TaoLiSystem/static/setting.bin", "rb")

# 记录原本按钮绑定函数
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed

# 设置项对应设置
settings = [["无线网络选项", "调整互联网设置", 0, 'connect_setting'],  # 名称 介绍 gui图片在文件setting.bin中对应的位置 执行函数名
            ["日期时间选项", "调整日期时间", 78, 'date_setting'],
            ["掌控板选项", "设定掌控板偏好", 184, 'system_setting']]

# 按钮事件
def button_a_callback(_):
    global setting_id
    setting_id = min(len(settings) - 1, setting_id + 1)

# 按钮事件
def button_b_callback(_):
    global setting_id
    if setting_id == 0:
        setting_id = -1
        button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o  # 还原按钮绑定
        button_b.event_pressed(0)
        return
    setting_id = max(0, setting_id - 1)

button_a.event_pressed = button_a_callback
button_b.event_pressed = button_b_callback

def show():
    global setting_id, enter_time, exiting, tip1, tip2
    
    if tip1:
        tip1 = False
        if sysgui.messageBox("长按 P 进入设置项"):
            configData.write("system", "settingTipped", "1") 
    
    oled.fill(0)
    t = time.localtime()  # 用秒数来动态绘制
    
    if setting_id != len(settings) - 1:
        oled.DispChar("◀", 1, 24)
        oled.DispChar("A", 13, 24)
    if setting_id != 0:
        oled.DispChar("▶", 114, 24)
        oled.DispChar("B", 106, 24)
    else:
        oled.DispChar("B>", 114, 0)
    
    # 设置项绘制
    sysgui.draw_string_center(settings[setting_id][0], 34)
    # 图标绘制
    bin2picture.print_from_bin_by_pos(128 // 2  - 32 // 2, 3, gui_fp, settings[setting_id][2])

    oled.show()
    
    _ = setting_id
    # 等待按钮事件
    while _ == setting_id:   # 改变说明按键中断，改变了 setting_id 的值
        time.sleep_ms(100)
        oled.show()
        
        # 提示背景
        oled.fill_rect(0, 49, int(128 * (enter_time / 3)), 64, 1)
        
        # 判断是否按下触摸按键
        if touchPad_P.read() < touchPad_sensitivity:
            enter_time -= 1
            
            # 提示背景
            oled.fill_rect(0, 49, int(128 * (enter_time / 3)), 64, 1)
            sysgui.draw_string_center("进入还需长按 %d 秒" % (enter_time), 49, mode=TextMode.rev)
            
            if enter_time <= 0:
                enter_time = 3
                
                # 是否已经提示过如何使用选择页面
                if tip2:
                    tip2 = False
                    if sysgui.messageBox("在设置选择页面\nP/N键切换选项", yes_text="下一步"):
                        sysgui.messageBox("T选择第一个\nH选择最后一个", yes_text="下一步")
                        sysgui.messageBox("A按钮确认\nB按钮取消")
                        configData.write("system", "itemSelectorTipped", "1")  
                getattr(settingFun, settings[setting_id][3])()
                break  # 立刻刷新页面
            
        else:
            enter_time = 3
            
            sysgui.draw_string_center(settings[setting_id][1], 49, mode=TextMode.rev)
            
        

    return 0
    
def close():
    if 'TaoLiSystem.page.settingFun' in sys.modules:
        del sys.modules['TaoLiSystem.page.settingFun']
    gui_fp.close()





