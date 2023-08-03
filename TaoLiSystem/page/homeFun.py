# 主页的功能实现
import time
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

# 绘制时间所需字体文件
albbhp_font_fp = open("TaoLiSystem/static/font_albbhp.bin", "rb")
albbhp_map = {':': 919, '0': 525, '1': 574, '2': 611, '3': 646, '4': 683, '5': 724, '6': 759, '7': 800, '8': 835, '9': 878}
weekday_abbr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

# 绘制 GUI 所需的文件
gui_fp = open("TaoLiSystem/static/home.bin", "rb")
gui_map = {'bulb': 0}

recoder_times = []

def drawStopwatch():
    """秒表"""
    exit_var = False  # 标记是否退出
    
    # 用于对于先前按钮的记录
    button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮
    
    previousTime = 0
    previousTime_recoder = 0
    start = False
    
    def draw_running():
        nonlocal previousTime_recoder
        oled.fill(0)
        sysgui.draw_string_center("秒表", 0)
        string_time = utils.convert_ms_to_hms(previousTime_recoder)
        oled.DispChar("%02d:%02d:%02d:%02d" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 30, 16)
        sysgui.draw_string_center("<A 停止>  <B 记录>", 32)
        if recoder_times:
            
            string_time = utils.convert_ms_to_hms(recoder_times[-1])
            sysgui.draw_string_center("%02d:%02d:%02d:%02d" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 48)
        else:
            sysgui.draw_string_center("[这里会展示最新记录]", 48)
        
    def draw_stopping():
        nonlocal previousTime_recoder
        oled.fill(0)
        sysgui.draw_string_center("秒表", 0)
        string_time = utils.convert_ms_to_hms(previousTime_recoder)
        oled.DispChar("%02d:%02d:%02d:%02d" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 30, 16)
        sysgui.draw_string_center("<A 继续>  <B 归零>", 32)
        if recoder_times:
            string_time = utils.convert_ms_to_hms(recoder_times[-1])
            sysgui.draw_string_center("[%02d:%02d:%02d:%02d]" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 48)
        else:
            sysgui.draw_string_center("[这里会展示最新记录]", 48)

    def draw_start():
        oled.fill(0)
        sysgui.draw_string_center("秒表", 0)
        oled.DispChar("%02d:%02d:%02d:%02d" % (0, 0, 0, 0), 30, 16)
        sysgui.draw_string_center("<A 开始>  <B 退出>", 32)
        if recoder_times:
            string_time = utils.convert_ms_to_hms(recoder_times[-1])
            sysgui.draw_string_center("[%02d:%02d:%02d:%02d]" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 48)
        else:
            sysgui.draw_string_center("[这里会展示最新记录]", 48)
    
    def button_a_callback(_):
        nonlocal start, previousTime
        a_pressed = True
        start = not start
        if start:
            previousTime = time.ticks_ms()
            sysgui.draw_rect_empty(1, 1, 126, 62, draw_running)
            oled.show()
        else:
            sysgui.draw_rect_empty(1, 1, 126, 62, draw_stopping)
        
    def button_b_callback(_):
        nonlocal exit_var, previousTime_recoder, start
        b_pressed = True
        
        if not start and previousTime_recoder != 0:
            previousTime_recoder = 0
            sysgui.draw_rect_empty(1, 1, 126, 62, draw_start)
            recoder_times.clear()
            oled.fill_rect(0, 48, 128, 64, 0)
            sysgui.draw_string_center("[这里会展示最新记录]", 48)
            sysgui.draw_rect_empty(1, 1, 126, 62, no_fill=True)
            oled.show()
        elif not start:
            exit_var = True
            button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
        elif start:
            recoder_times.append(previousTime_recoder)
            oled.fill_rect(0, 48, 128, 64, 0)
            if recoder_times:
                string_time = utils.convert_ms_to_hms(recoder_times[-1])
                sysgui.draw_string_center("[%02d:%02d:%02d:%02d]" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 48)
            else:
                sysgui.draw_string_center("[这里会展示最新记录]", 48)
            sysgui.draw_rect_empty(1, 1, 126, 62, no_fill=True)
    
    button_a.event_pressed, button_b.event_pressed = button_a_callback, button_b_callback
    
    # 不变的内容
    oled.fill(0)
    sysgui.draw_rect_empty(1, 1, 126, 62, draw_start)
    oled.show()
    
    while not exit_var:
        
        if start:
            previousTime_recoder += time.ticks_ms() - previousTime
            previousTime = time.ticks_ms()
            string_time = utils.convert_ms_to_hms(previousTime_recoder)
            oled.DispChar("%02d:%02d:%02d:%02d" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10), 30, 16)
            oled.show()
            continue
        
        while not exit_var and not start:
            if touchPad_P.read() <= touchPad_sensitivity:
                _ = []
                for r in recoder_times:
                    string_time = utils.convert_ms_to_hms(r)
                    _.insert(0, "%02d:%02d:%02d:%02d" % (string_time[0], string_time[1], string_time[2], string_time[3] // 10))
                sysgui.itemSelector("历史记录", _)
                sysgui.draw_rect_empty(1, 1, 126, 62, draw_stopping)
                oled.show()