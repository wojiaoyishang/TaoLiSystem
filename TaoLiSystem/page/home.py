# 负责主页面绘制
import sys
import time
from mpython import *

from TaoLiSystem.core import sysgui
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

from TaoLiSystem.page.homeFun import *

# 清理一下掌控板启动完毕之后的内存冗余
gc.collect()

# 用于熄屏倒计时
if configData.read("system", "ScreenOffStatus") == "1":
    screenOff_timeout_setting = int(configData.read("system", "ScreenOffTimeout"))
else:
    screenOff_timeout_setting = -1
screenOff_timeout = screenOff_timeout_setting

# 记录上一时刻时间
pre_time = time.localtime()

# 用于对于先前按钮的记录
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮

# 主页是否需要提示
tip = configData.read("system", "homeTipped") != "1"
if tip:
    sysgui.messageBox("你好呀~\n欢迎使用陶丽系统。", yes_text="你好？")
    sysgui.messageBox("看来你是第一次\n使用这个系统。", yes_text="嗯嗯")
    sysgui.messageBox("那让我偷偷告诉你\n在主页按AB键可以\n切换页面哦！", yes_text="我明白了")
    configData.write("system", "homeTipped", "1")

# 熄屏唤醒
def button_callback(_):
    global button_a_callback_o, button_b_callback_o, screenOff_timeout
    screenOff_timeout = screenOff_timeout_setting
    oled.poweron()
    oled.show()
    button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o  # 还原按钮

def show():
    global pre_time, screenOff_timeout
    
    
    t = time.localtime()
    
    # 熄屏逻辑
    if pre_time[5] != t[5]:
        if screenOff_timeout == 0:
            oled.poweroff()  # 关闭电源
            button_a.event_pressed, button_b.event_pressed = button_callback, button_callback  # 禁用原先的按钮
            return
        elif screenOff_timeout != -1:
            screenOff_timeout -= 1
            
    oled.fill(0)
    
    # 图标绘制
    bin2picture.print_from_bin_by_pos(10, 1, gui_fp, gui_map['bulb'])
    
    # 时间绘制
    sysgui.draw_string_from_bin(66, 6, albbhp_font_fp, "%02d" % (t[3]), albbhp_map)
    sysgui.draw_string_from_bin(94, 6, albbhp_font_fp, "%02d" % (t[4]), albbhp_map)
    if t[5] % 2:     
        sysgui.draw_string_from_bin(87, 5, albbhp_font_fp, ":", albbhp_map)


    oled.DispChar("%s" % (weekday_abbr[t[6]]), 68, 26)
    oled.DispChar("%02d" % (t[5]), 102, 26)

    # 日期绘制
    oled.fill_rect(0, 49, 128, 64, 1)
    sysgui.draw_string_center("%04d年%02d月%02d日" % (t[0], t[1], t[2]), 49, mode=TextMode.rev)

    # 进度条绘制
    oled.line(0, 0, 128 - int(128 * (t[5] / 60)), 0, 1)

    # 框框的绘制
    oled.rect(0, 1, 128, 63, 1)
    # oled.line(61, 1, 61, 49, 1)
    
    # 判断是否按下触摸按键
    if touchPad_P.read() <= touchPad_sensitivity :
        drawStopwatch()
        screenOff_timeout = screenOff_timeout_setting
    elif touchPad_Y.read() <= touchPad_sensitivity :
        randomINT()
        screenOff_timeout = screenOff_timeout_setting
    
    oled.show()
    pre_time = t
    
def close():
    if 'TaoLiSystem.page.homeFun' in sys.modules:
        del sys.modules['TaoLiSystem.page.homeFun']
    albbhp_font_fp.close()
    gui_fp.close()
