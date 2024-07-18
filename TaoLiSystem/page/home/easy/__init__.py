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

# **********************************变量定义**********************************
# 记录上一时刻时间
pre_time = time.localtime()

# 绘制时间所需字体文件
albbhp_font_fp = open("TaoLiSystem/static/font_albbhp.bin", "rb")
albbhp_map = {':': 919, '0': 525, '1': 574, '2': 611, '3': 646, '4': 683, '5': 724, '6': 759, '7': 800, '8': 835, '9': 878}
weekday_abbr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

# 用于对于先前按钮的记录
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮

# ===================================初始化桌面结束===================================

def show():
    global pre_time, screenOff_timeout
    
    t = time.localtime()
    
    # ==================================基本熄屏逻辑开始==================================
    # 熄屏逻辑
    if pre_time[5] != t[5]:
        if ScreenOffTimeout != -1 and screenOff_countdown <= 0:
            oled.poweroff()  # 关闭电源
            
            button_a.event_pressed, button_b.event_pressed = button_callback, None  # 禁用原先的按钮
            if ScreenOffStatus_sleep:  # 进入深度睡眠
                print("已进入浅度睡眠。")
                utils.lightsleep_irc(tip=False)
                time.sleep_ms(100)  # 等一手
                button_callback(0)  # 模拟亮屏启动
            
            return
        elif ScreenOffTimeout != -1:
            screenOff_countdown -= 1
    # ==================================基本熄屏逻辑结束==================================
    
    # ==================================主要界面元素绘制开始==================================
    # 时间绘制
    oled.fill(0)
    sysgui.draw_string_from_bin(38, 12, albbhp_font_fp, "%02d" % (t[3]), albbhp_map)
    
    sysgui.draw_string_from_bin(70, 12, albbhp_font_fp, "%02d" % (t[4]), albbhp_map)
    
    if t[5] % 2:     
        sysgui.draw_string_from_bin(62, 10, albbhp_font_fp, ":", albbhp_map)
    
    # 日期
    sysgui.draw_string_center("%04d年%02d月%02d日" % (t[0], t[1], t[2]), 38)
    
    oled.show()
    # ==================================主要界面元素绘制结束==================================
    
    pre_time = t

def button_callback(_):  # 熄屏唤醒
    global button_a_callback_o, button_b_callback_o, screenOff_countdown, ScreenOffTimeout
    button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o  # 还原按钮
    screenOff_countdown = ScreenOffTimeout
    oled.poweron()
    oled.show()

def setting():
    # ===========================个性化设置===========================
    while True:
        settings = []
        
        settings.append("关于此主页")
        
        choice = sysgui.itemSelector("个性化设置", settings)
        if choice == 0:
            sysgui.tipBox("简单页面示例")
        else:
            break
    # ===========================个性化设置===========================
    return

def close():
    albbhp_font_fp.close()


