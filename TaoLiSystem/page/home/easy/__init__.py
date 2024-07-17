# 负责主页面绘制
import sys
import time
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

# 清理一下掌控板启动完毕之后的内存冗余
utils.gc_collect()

# 用于熄屏倒计时
if configData.read("system", "ScreenOffStatus") == "1" and configData.read("system", "ScreenOffTimeout") != "0":
    screenOff_timeout_setting = int(configData.read("system", "ScreenOffTimeout", "-1"))
else:
    screenOff_timeout_setting = -1
screenOff_timeout = screenOff_timeout_setting

# 记录上一时刻时间
pre_time = time.localtime()

# 用于对于先前按钮的记录
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮

# 绘制时间所需字体文件
albbhp_font_fp = open("TaoLiSystem/static/font_albbhp.bin", "rb")
albbhp_map = {':': 919, '0': 525, '1': 574, '2': 611, '3': 646, '4': 683, '5': 724, '6': 759, '7': 800, '8': 835, '9': 878}
weekday_abbr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

# 熄屏唤醒
def button_callback(_):
    global button_a_callback_o, button_b_callback_o, screenOff_timeout
    button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o  # 还原按钮
    screenOff_timeout = screenOff_timeout_setting
    oled.poweron()
    oled.show()

def show():
    global pre_time, screenOff_timeout
    
    t = time.localtime()
    
    # 熄屏逻辑
    if pre_time[5] != t[5]:
        if screenOff_timeout != -1 and screenOff_timeout <= 0:
            oled.poweroff()  # 关闭电源
            button_a.event_pressed, button_b.event_pressed = button_callback, button_callback  # 禁用原先的按钮
            return
        elif screenOff_timeout != -1:
            screenOff_timeout -= 1
            
    

    # 时间绘制
    oled.fill(0)
    sysgui.draw_string_from_bin(38, 12, albbhp_font_fp, "%02d" % (t[3]), albbhp_map)
    
    sysgui.draw_string_from_bin(70, 12, albbhp_font_fp, "%02d" % (t[4]), albbhp_map)
    
    if t[5] % 2:     
        sysgui.draw_string_from_bin(62, 10, albbhp_font_fp, ":", albbhp_map)
    
    # 日期
    sysgui.draw_string_center("%04d年%02d月%02d日" % (t[0], t[1], t[2]), 38)

    oled.show()
    pre_time = t

def setting():
    pass
    return

def close():
    albbhp_font_fp.close()


