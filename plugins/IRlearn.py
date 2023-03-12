# {"Name": "遥控红外学习","Version": "v0.0.1","Master": "以赏", "Description": "学习遥控信号，前提是安装了拓展版。学习的内容会放在 TaoLiSystem/data/IRlearn 文件夹中。", "More": "由以赏制作"}

from mpython import *
import parrot
import time
import os
import json

import TaoLiSystem.function

from TaoLiSystem.ItemSelector import ItemSelector as ItemSelector
from TaoLiSystem.morseType import MorseType as MorseType

# def on_button_a_pressed(_):
#     global data
#     ir.learn()
#     time.sleep(4)
#     if 0 == ir.__get_learn_status():
#         data = ir.get_learn_data()
#         print(data)
#         oled.fill(0)
#         oled.DispChar("成功", 0, 0)
#         oled.show()
#     else:
#         print('什么都没学到...')
# 
# button_a.event_pressed = on_button_a_pressed
# 
# def on_button_b_pressed(_):
#     global data
#     print(data)
#     ir.send(data, 0)
#     oled.fill(0)
#     oled.DispChar("发送！" + str(time.time()), 0, 0)
#     oled.show()
# 
# button_b.event_pressed = on_button_b_pressed
# 
# ir = parrot.IR()
# data = None

ir = parrot.IR()
try:
    with open("TaoLiSystem/data/IRlearn/fastKey.json", "r") as f:
        fastKey = json.loads(f.read())
except:
    fastKey = {}

try:
    # 查看是否存在 data 文件夹
    os.mkdir("TaoLiSystem/data")
except:
    pass

try:
    # 查看是否存在 IRlearn 文件夹
    os.mkdir("TaoLiSystem/data/IRlearn")
except:
    pass

def learn(name=False):
    """学习红外"""
    try:
        TaoLiSystem.function.loadingPage("请确认打开拓展板电源，", 3, 5)
        oled.show()
        time.sleep(1)
        TaoLiSystem.function.loadingPage("并对准拓展板 IR 5s", 10, 5)
        oled.show()
        time.sleep(1)
        TaoLiSystem.function.waitingPage("正在", "学习", "OvO")
        oled.show()
        ir.learn()
        time.sleep(5)
        if ir.__get_learn_status() == 0:
            data = ir.get_learn_data()
            oled.fill(0)
            TaoLiSystem.function.waitingPage("学习", "成功", "了哦")
            oled.show()
            time.sleep(3)
            if not name:
                name = MorseType("给数据取个名字！").start()
            try:
                with open("TaoLiSystem/data/IRlearn/" + name + ".data", "wb") as f:
                    f.write(data)
                    print(data)
                TaoLiSystem.function.waitingPage("保存", "成功", "了哦")
                oled.show()
                time.sleep(3)
            except:
                TaoLiSystem.function.waitingPage("保存", "失败", "QAQ")
                oled.show()
                time.sleep(3)
        else:
            TaoLiSystem.function.waitingPage("没有", "数据", "QAQ")
            oled.show()
            time.sleep(3)
    except:
        TaoLiSystem.function.loadingPage("拓展板电源未开启！", 10, 5)
        oled.show()
        time.sleep(3)
        
def read():
    """读取"""
    global fastKey
    _ = os.listdir("TaoLiSystem/data/IRlearn")
    try:
        _.remove("fastKey.json")
    except:
        pass
    path = "TaoLiSystem/data/IRlearn/" + ItemSelector(_, "学习的数据").start()
    if path in ("TaoLiSystem/data/IRlearn/", ""):
        return
    
    k = dict(zip(fastKey.values(), fastKey.keys())).get(path, "")
    
    with open(path, "rb") as f:
        data = f.read()
    
    keep_send = False
    while True:
        action = ItemSelector(["发送", "持续发送" if not keep_send else "停止持续发送", "设置快捷键", "修改", "删除"], "操作" if k == "" else "操作 Key:" + k).start()
        if action == "":
            break
        elif action == "发送":
            try:
                ir.send(data)
            except:
                pass
        elif action in ("持续发送", "停止持续发送"):
            if keep_send == False:
                ir.send(data, 1)
                keep_send = True
            else:
                ir.stop_send()
                keep_send = False
        elif action == "删除":
            os.remove(path)
            break
        elif action == "设置快捷键":
            k = ItemSelector(["P", "Y", "T", "H", "O", "N"], "选择快捷键").start()
            if k == "":
                continue
            fastKey[k] = path
            try:
                with open("TaoLiSystem/data/IRlearn/fastKey.json", "w") as f:
                        f.write(json.dumps(fastKey))
                TaoLiSystem.function.waitingPage("设置", "成功", "了哦")
                oled.show()
            except:
                TaoLiSystem.function.waitingPage("设置", "失败", "惹..")
                oled.show()
            time.sleep(3)
        elif action == "修改":
            learn(path[path.rfind("/") + 1:path.rfind(".")])
            return

def sendFromFile(path):
    try:
        with open(path, "rb") as f:
            r.send(f.read(), 0)
    except:
        pass

def fastKeyMode():
    """快捷键模式"""
    global fastKey
    
    while True:
        oled.fill(0)
        oled.DispChar("按下 B 退出，P - N 为您设置的快捷键", 0, 0, 1, True)
        oled.show()
        
        while True:
            time.sleep(0.05)
            if button_b.value() == 0:
                return
            
            if touchPad_P.read() <= 400:
                sendFromFile(fastKey["P"])
            elif touchPad_Y.read() <= 400:
                sendFromFile(fastKey["Y"])
            elif touchPad_T.read() <= 400:
                sendFromFile(fastKey["T"])
            elif touchPad_H.read() <= 400:
                sendFromFile(fastKey["H"])
            elif touchPad_O.read() <= 400:
                sendFromFile(fastKey["O"])
            elif touchPad_N.read() <= 400:
                sendFromFile(fastKey["N"])
while True:
    action = ItemSelector(["学习", "读取", "快捷键模式"], "遥控红外学习").start()
    if action == "":
        break
    elif action == "学习":
        learn()
    elif action == "读取":
        read()
    elif action == "快捷键模式":
        fastKeyMode()
    

