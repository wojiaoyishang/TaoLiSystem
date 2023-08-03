import os
import gc
import uio
import sys
import json
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.modules import bin2picture
from TaoLiSystem.core.config import *

# 用于对于先前按钮的记录
button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮
button_a.event_pressed, button_b.event_pressed = None, None

def show():
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
                print("* 有效插件 %s (%s): %s" % (file_info[0], info['name'], info['description']))
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
    selected_id = 0
    while True:  
        selected_id = sysgui.itemSelector("选择插件", plugins_name, selected_id=selected_id)
        
        if selected_id is None:
            button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
            button_a.event_pressed(0)
            break
        
        # 获取这个插件的信息
        with open("TaoLiSystem/plugins/" + plugins_folder[selected_id] + "/__init__.json") as f:
            info = json.load(f)
        
        description = info['description']
        
        del info
        gc.collect()
        
        while True:
            option_id = sysgui.itemSelector("插件(%s)" % plugins_name[selected_id], ["加载插件", "查看介绍", "删除插件"])
            
            if option_id is None:
                break
                
            if option_id == 0:
                gc.collect()  # 加载前摇
                print("* 加载插件 %s (%s)，RAM:%d" % (plugins_folder[selected_id], plugins_name[selected_id], gc.mem_free()))
                imported_modules_before = list(sys.modules.keys())
                imported_module = utils.importModule("TaoLiSystem.plugins." + plugins_folder[selected_id])

                del imported_module
                print("* 插件 %s (%s) 加载完成，清理中......" % (plugins_folder[selected_id], plugins_name[selected_id]))
                # 删除加载的所有内容
                for m in list(sys.modules.keys()):
                    if m not in imported_modules_before:
                        del sys.modules[m]
                        print("* 删除多加载模块:%s" % m)
                
                del m, option_id
                gc.collect()
                print("* 插件 %s (%s) 完毕，RAM:%d" % (plugins_folder[selected_id], plugins_name[selected_id], gc.mem_free()))
                break
            elif option_id == 1:
                text_buffer = uio.StringIO(description)
                sysgui.txtStreamReader(text_buffer, "%s (%s)" % (plugins_folder[selected_id], plugins_name[selected_id]))
                text_buffer.close()
                
                del text_buffer
            elif option_id == 2:
                if sysgui.messageBox("你确定要删除吗？", yes_text="是的", no_text="不是"):
                    sysgui.tipBox("删除中......")
                    utils.delete_folder("TaoLiSystem/plugins/" + plugins_folder[selected_id])
                    break
                
                
def close():
    return

