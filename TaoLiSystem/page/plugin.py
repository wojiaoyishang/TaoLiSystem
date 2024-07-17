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

    t = time.localtime()  # 用秒数来动态绘制
    
    sysgui.tipBox("正在获取信息......", 0)
    
    oled.fill(0)
    
    if plugin_id != 0:
        oled.DispChar("◀", 1, 24)
        oled.DispChar("A", 13, 24)
    if plugin_id != len(plugins_name) - 1:
        oled.DispChar("▶", 114, 24)
        oled.DispChar("B", 106, 24)
    if plugin_id == 0:
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
        time.sleep_ms(100)
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
    
    selection_id = sysgui.itemSelector("运行插件", ["直接加载", "重启到初始化后加载", "重启到初始化前加载"])
    
    if selection_id is None:
        return
    
    if selection_id == 1:
        # 重启执行
        f = open("bootconfig", "w")
        f.write('{"mode": "pluginrun", "module": "' + plugins_folder[plugin_id] + '", "priority": 1}')
        f.close()
        import machine
        machine.reset()
    elif selection_id == 2:
        # 重启执行
        f = open("bootconfig", "w")
        f.write('{"mode": "pluginrun", "module": "' + plugins_folder[plugin_id] + '", "priority": 0}')
        f.close()
        import machine
        machine.reset()
    
    sysgui.tipBox("打开插件中......", 0)
    gc.collect()  # 加载前摇
    print("* 加载插件 %s (%s)，RAM:%d" % (plugins_folder[plugin_id], plugins_name[plugin_id], gc.mem_free()))
    imported_modules_before = list(sys.modules.keys())
    
    # 记录原先按钮事件
    button_a_callback_o1, button_b_callback_o1 = button_a.event_pressed, button_b.event_pressed
    button_a.event_pressed, button_b.event_pressed = None, None
    try:
        imported_module = utils.importModule("TaoLiSystem.plugins." + plugins_folder[plugin_id])
        # 记录保留的模块
        try:
            KEEP_MODULES = imported_module.KEEP_MODULES.copy()
        except AttributeError:
            KEEP_MODULES = []
        
    except BaseException as e:
        print("-" * 30)
        buffer = uio.StringIO()
        sys.print_exception(e, buffer)
        traceback_str = buffer.getvalue()
        buffer.close()
        
        print("* 插件运行时抛出了一个错误: ")
        print(traceback_str, end="")
        print("-" * 30)
        
        KEEP_MODULES = []
    sysgui.tipBox("清理内存中......", 0)
    # 还原
    button_a.event_pressed, button_b.event_pressed = button_a_callback_o1, button_b_callback_o1

    print("* 插件 %s (%s) 加载完成，清理中...... (RAM:%d)" % (plugins_folder[plugin_id], plugins_name[plugin_id], gc.mem_free()))
    print("* 保留模块列表:", KEEP_MODULES)
    # 删除加载的所有内容
    utils.compare_and_clean_modules(imported_modules_before, KEEP_MODULES)
            
    # 如果动态改变了保留的模块
    if 'keep_modules' in global_var and plugins_folder[plugin_id] in global_var['keep_modules']:
        for m in global_var['keep_modules'][plugins_folder[plugin_id]]:
            if m not in KEEP_MODULES:
                keep = False
                # 看看其它插件有没有保留
                for other_f in global_var['keep_modules'].keys():
                    if other_f != plugins_folder[plugin_id] and m in global_var['keep_modules'][other_f]:
                        keep = True
                if keep:
                    continue
        
                i = 0
                if sys.modules[m] == imported_module:
                    imported_module = None
                    for l in dir(sys.modules[m]):
                        try:
                            setattr(sys.modules[m], l, None)
                            i += 1
                            # print("* 删除多加载模块对象:%s %s" % (m, l))
                        except AttributeError:
                            continue
                del sys.modules[m]
                gc.collect()
                print("* 删除保留模块:%s (对象个数:%d) (RAM:%d)" % (m, i, gc.mem_free()))
    
        global_var['keep_modules'][plugins_folder[plugin_id]] = KEEP_MODULES
    
    if 'keep_modules' not in global_var:
        global_var['keep_modules'] = {}
    
    if len(KEEP_MODULES) != 0:
        global_var['keep_modules'][plugins_folder[plugin_id]] = KEEP_MODULES
    elif plugins_folder[plugin_id] in global_var['keep_modules']:
        del global_var['keep_modules'][plugins_folder[plugin_id]]
    
    if len(global_var['keep_modules']) == 0:
        del global_var['keep_modules']
                
    del m, button_a_callback_o1, button_b_callback_o1, i, KEEP_MODULES
    gc.collect()
    print("* 插件 %s (%s) 完毕，RAM:%d" % (plugins_folder[plugin_id], plugins_name[plugin_id], gc.mem_free()))

def close():
    return
