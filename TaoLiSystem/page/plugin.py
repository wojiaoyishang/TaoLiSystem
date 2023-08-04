import os
import gc
import uio
import sys
import json
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

# 是否需要提示
tip1 = configData.read("system", "settingTipped") != "1"  # 设置选择页面

# 用于对于先前按钮的记录
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮

# 目前插件项
plugin_id = 0
enter_time = 3  # 进入设置项倒计时
sysgui.tipBox("正在加载插件......", 0)
    
# 遍历 plugins 文件夹
plugins_folder = []
plugins_name = []
for file_info in os.ilistdir("TaoLiSystem/plugins"):
    path = "TaoLiSystem/plugins/" + file_info[0]
    if file_info[1] == 16384:  # 是文件夹
        try:
            with open(path + "/__init__.json") as f:
                info = json.load(f)
            plugins_name.append(info['name'])
            plugins_folder.append(file_info[0])
            print("* 有效插件 %s (%s): %s(%s)" % (file_info[0], info['name'], info['description'], info['brief']))
        except OSError:  # 文件不存在
            print("* 插件目录%s中，自述文件不存在。" % path)
            continue
        except ValueError:  # JSON格式不合法
            print("* 插件目录%s中，自述文件格式错误。" % path)
            continue
        except KeyError:  # 自述文件缺少值
            print("* 插件目录%s中，自述文件缺少信息。" % path)
            continue

del path, file_info, info  # 能省一点是一点

def button_a_callback(_):
    global plugin_id
    if plugin_id == 0:
        plugin_id = -1
        button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
        button_a.event_pressed(0)
        return
    plugin_id = max(0, plugin_id - 1)

def button_b_callback(_):
    global plugin_id, plugins_name
    plugin_id = min(len(plugins_name) - 1, plugin_id + 1)

button_a.event_pressed, button_b.event_pressed = button_a_callback, button_b_callback

def show():
    global tip1, enter_time, plugin_id, plugins_name, plugins_folder

    if tip1:
        tip1 = False
        if sysgui.messageBox("长按 P 进入插件"):
            configData.write("system", "settingTipped", "1") 
    
    oled.fill(0)
    t = time.localtime()  # 用秒数来动态绘制
    
    if plugin_id != 0:
        oled.DispChar("◀", 1, 24)
        oled.DispChar("A", 13, 24)
    if plugin_id != len(plugins_name) - 1:
        oled.DispChar("▶", 114, 24)
        oled.DispChar("B", 106, 24)
    else:
        oled.DispChar("<A", 0, 0)
    
    # 获取插件信息
    with open("TaoLiSystem/plugins/" + plugins_folder[plugin_id] + "/__init__.json") as f:
        info = json.load(f)
    
    if 'ico_bin' in info and info['ico_bin'].strip() != "" and 'ico_pos' in info:
        ico_bin = info['ico_bin']
        ico_pos = info['ico_pos']
    else:
        ico_bin = None
        ico_pos = None
    
    # 绘制插件项
    if ico_bin:
        with open("TaoLiSystem/plugins/" + plugins_folder[plugin_id] + "/" + ico_bin, "r") as f:
            if isinstance(ico_pos, int):
                bin2picture.print_from_bin_by_pos(128 // 2  - 32 // 2, 3, f, ico_pos)
            else:
                bin2picture.print_from_bin(128 // 2  - 32 // 2, 3, f, ico_pos)
        sysgui.draw_string_center(plugins_name[plugin_id], 34)
    else:
        sysgui.draw_string_center(plugins_name[plugin_id], 18)
    
    
    
    oled.show()
    
    # 等待触摸事件
    _ = plugin_id
    while _ == plugin_id:     
        time.sleep(0.1)
        oled.show()
        
        # 提示背景
        oled.fill_rect(0, 49, int(128 * (enter_time / 3)), 64, 1)
        
        # 判断是否按下触摸按键
        if touchPad_P.read() < touchPad_sensitivity:
            enter_time -= 1
            
            # 提示背景
            oled.fill_rect(0, 49, int(128 * (enter_time / 3)), 64, 1)
            sysgui.draw_string_center("加载还需长按 %d 秒" % (enter_time), 49, mode=TextMode.rev)
            
            if enter_time <= 0:
                enter_time = 3
                
                # 加载插件
                load_plugin()
                
                break
        elif touchPad_N.read() < touchPad_sensitivity:
            enter_time -= 1
            
            # 提示背景
            oled.fill_rect(0, 49, int(128 * (enter_time / 3)), 64, 1)
            sysgui.draw_string_center("详情还需长按 %d 秒" % (enter_time), 49, mode=TextMode.rev)
            
            if enter_time <= 0:
                enter_time = 3
                # 加载介绍
                text_buffer = uio.StringIO("插件名称:" + plugins_name[plugin_id] + "\n" + \
                                           "插件文件夹:" + plugins_folder[plugin_id] + "\n" + \
                                           "插件作者:" + info['author'] + "\n" + \
                                           "插件版本:" + info['version'] + "\n" + \
                                           "插件简介:" + info['brief'] + "\n" + \
                                           "插件介绍:" + info['description'])
                sysgui.txtStreamReader(text_buffer, plugins_name[plugin_id])
                text_buffer.close()
                
                break
        else:
            enter_time = 3
            sysgui.draw_string_center(info['brief'], 49, mode=TextMode.rev)
            
    return

def load_plugin():
    global plugin_id, plugins_folder, plugins_name
    
    gc.collect()  # 加载前摇
    print("* 加载插件 %s (%s)，RAM:%d" % (plugins_folder[plugin_id], plugins_name[plugin_id], gc.mem_free()))
    imported_modules_before = list(sys.modules.keys())
    imported_module = utils.importModule("TaoLiSystem.plugins." + plugins_folder[plugin_id])

    del imported_module
    print("* 插件 %s (%s) 加载完成，清理中......" % (plugins_folder[plugin_id], plugins_name[plugin_id]))
    # 删除加载的所有内容
    for m in list(sys.modules.keys()):
        if m not in imported_modules_before:
            del sys.modules[m]
            print("* 删除多加载模块:%s" % m)
    
    del m
    gc.collect()
    print("* 插件 %s (%s) 完毕，RAM:%d" % (plugins_folder[plugin_id], plugins_name[plugin_id], gc.mem_free()))

def close():
    return

show()