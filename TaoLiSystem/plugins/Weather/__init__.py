# 主页天气页面
import sys

from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

from .weatherFun import *


# 退出定义
exit_weather = False

# 按钮事件
def button_callback(_):
    global exit_weather
    exit_weather = True


button_a.event_pressed, button_b.event_pressed = button_callback, button_callback

def show():
    sysgui.draw_rect_empty(1, 1, 126, 62, draw_main)
    oled.show()

    while not exit_weather and global_var.get("weather_got"):
        if touchPad_P.read() <= touchPad_sensitivity or time.time() - global_var.get('daily_weather_time', time.time()) >= 300:  # 5分钟刷新
            if 'daily_weather' in global_var:
                del global_var['daily_weather']
            break
        elif touchPad_Y.read() <= touchPad_sensitivity:
            sysgui.draw_rect_empty(1, 1, 126, 62, lambda : draw_pre(0))
            oled.show()
            while touchPad_Y.read() <= touchPad_sensitivity:
                pass
            return
        elif touchPad_T.read() <= touchPad_sensitivity:
            sysgui.draw_rect_empty(1, 1, 126, 62, lambda : draw_pre(1))
            oled.show()
            while touchPad_T.read() <= touchPad_sensitivity:
                pass
            return
        elif touchPad_H.read() <= touchPad_sensitivity:
            sysgui.draw_rect_empty(1, 1, 126, 62, lambda : draw_pre(2))
            oled.show()
            while touchPad_H.read() <= touchPad_sensitivity:
                pass
            return
        elif touchPad_O.read() <= touchPad_sensitivity:
            sysgui.draw_rect_empty(1, 1, 126, 62, lambda : draw_suggest())
            oled.show()
            while touchPad_O.read() <= touchPad_sensitivity:
                pass
            return
        elif touchPad_N.read() <= touchPad_sensitivity:
            while True:
                select_id = sysgui.itemSelector("天气获取设置", ["设置城市", "还原默认", "目前城市：" + configData.read("weather", "location", "ip")])
                if select_id is None:
                    break
                
                if select_id == 0:
                    sysgui.messageBox("需要输入新的城市，\n城市设置查看\n知心天气文档。")
                    value = sysgui.textTypeBox()
                    configData.write("weather", "location", value)
                    sysgui.tipBox("修改成功。", 1)
                    break
                elif select_id == 1:
                    configData.write("weather", "location", "ip")
                    
            return
    
    while global_var.get("weather_got") is None and not exit_weather:
        if touchPad_P.read() <= touchPad_sensitivity:
            global_var["weather_got"] = True
            break
        
    if "wifi" in global_var and global_var.get("wifi").sta.isconnected() and not exit_weather:     
        oled.fill(0)
        sysgui.tipBox("正在获取天气......")
        oled.show()
        # 请求天气接口
        get_weather()
        return
    elif not exit_weather:
        oled.fill(0)
        sysgui.draw_rect_empty(1, 1, 126, 62, draw_error)
        oled.show()
        
while not exit_weather:
    show()
