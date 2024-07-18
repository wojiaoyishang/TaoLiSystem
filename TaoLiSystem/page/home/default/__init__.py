# 负责主页面绘制
import sys
import time
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

# ===================================开始初始化桌面===================================
from .function import *

# 清理一下掌控板启动完毕之后的内存冗余
utils.gc_collect()

# **********************************配置读取**********************************
# 用于熄屏倒计时
if configData.read("system", "ScreenOffStatus") == "1":  # 设置熄屏
    ScreenOffTimeout = int(configData.read("system", "ScreenOffTimeout", "-1"))
    ScreenOffStatus_sleep = int(configData.read("system", "ScreenOffStatus_sleep", "0"))
else:  # 没有设置熄屏
    ScreenOffTimeout = -1
    ScreenOffStatus_sleep = 0  # 是否启用浅度睡眠熄屏

# screenOff_countdown 是拿来倒计时的
# ScreenOffTimeout 是预设的倒计时秒数，如果为 -1 说明没有启用熄屏
screenOff_countdown = ScreenOffTimeout

# 进度条类型
progress_type = configData.read("home", "progress_type", "countdown")

# **********************************变量定义**********************************
# 记录上一时刻时间
pre_time = time.localtime()

# 用于对于先前按钮的记录
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮

# **********************************新手提示**********************************
# 主页是否需要提示
tip = configData.read("system", "homeTipped") != "1"
if tip:
    sysgui.messageBox("你好呀~\n欢迎使用桃丽系统。", yes_text="你好？")
    sysgui.messageBox("看来你是第一次\n使用这个系统。", yes_text="嗯嗯")
    sysgui.messageBox("那让我偷偷告诉你\n在主页按AB键可以\n切换页面哦！", yes_text="我明白了")
    configData.write("system", "homeTipped", "1")

# ===================================初始化桌面结束===================================

def show():
    global pre_time, screenOff_countdown, ScreenOffTimeout
    
    t = time.localtime()
    
    # ==================================基本熄屏逻辑开始==================================
    if pre_time[5] != t[5]:
        if ScreenOffTimeout != -1 and screenOff_countdown <= 0:
            oled.poweroff()  # 关闭电源
            
            button_a.event_pressed, button_b.event_pressed = button_callback, None  # 禁用原先的按钮
            if ScreenOffStatus_sleep:  # 进入深度睡眠
                print("已进入浅度睡眠。")
                utils.lightsleep_irc(tip=False, callback=lambda: button_callback(0))
            
            return
        elif ScreenOffTimeout != -1: 
            screenOff_countdown -= 1
    # ==================================基本熄屏逻辑结束==================================
    
    # ==================================主要界面元素绘制开始==================================
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

    # 进度条绘制 感谢来自 罗米奇 的灵感
    if progress_type == "countdown":
        oled.line(0, 0, 128 - int(128 * (t[5] / 60)), 0, 1)
    else:
        oled.line(0, 0, int(128 * (t[5] / 60)), 0, 1)

    # 框框的绘制
    oled.rect(0, 1, 128, 63, 1)
    # oled.line(61, 1, 61, 49, 1)
    
    oled.show()
    # ==================================主要界面元素绘制结束==================================
    
    # ==================================其他功能逻辑开始==================================
    # 判断是否按下触摸按键
    if touchPad_P.read() <= touchPad_sensitivity:
        drawStopwatch()
        screenOff_countdown = ScreenOffTimeout
    elif touchPad_Y.read() <= touchPad_sensitivity :
        randomINT()
        screenOff_countdown = ScreenOffTimeout
    elif touchPad_N.read() <= touchPad_sensitivity :
        statusShow()
        screenOff_countdown = ScreenOffTimeout
    # ==================================其他功能逻辑开始==================================
    
    pre_time = t

def button_callback(_):  # 熄屏唤醒
    global button_a_callback_o, button_b_callback_o, screenOff_countdown, ScreenOffTimeout
    screenOff_countdown = ScreenOffTimeout
    oled.poweron()
    button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o  # 还原按钮
    oled.show()

def setting():
    global progress_type
    # ===========================个性化设置===========================
    while True:
        settings = []
        
        if progress_type == "countdown":
            settings.append("进度条:倒计时")
        else:
            settings.append("进度条:正计时")
            
        settings.append("关于此主页")
        
        choice = sysgui.itemSelector("个性化设置", settings)
        if choice == 0:
            configData.write("home", "progress_type", "positive" if progress_type == "countdown" else "countdown")
            progress_type = "positive" if progress_type == "countdown" else "countdown"
        elif choice == 1:
            sysgui.tipBox("本质为真")
        else:
            break
    # ===========================个性化设置===========================
    return
    

def close():  # 销毁桌面
    albbhp_font_fp.close()
    gui_fp.close()

    
