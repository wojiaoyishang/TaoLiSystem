# bootloader 用于调试
import os
import time
import machine
import micropython
from mpython import *

# 设定最小RAM
micropython.alloc_emergency_exception_buf(4000)

if button_a.value() == 0 and button_b.value() == 0:  # 两个按钮同时按下
    while button_a.value() == 0 and button_b.value() == 0:
        pass
    while True:
        oled.DispChar("==Bootloader Menu==", 0, 0)
        oled.DispChar("<A> 运行备份的代码", 0, 16)
        oled.DispChar("<B> 继续代码运行", 0, 32)
        if button_a.value() == 0:
            try:  # 文件是否存在oDC
                os.rename("main.py.bak", "main.py.bak_")
            except OSError:
                oled.DispChar("main.py.bak文件不存在！或已经运行备份代码。", 0, 0, auto_return=True)
                time.sleep(3)
                oled.show()
                break
            
            os.rename("main.py", "main.py.main")  # 备份原来的文件
            os.rename("main.py.bak_", "main.py")  # 将备份文件变为现在的文件
            
            machine.reset()
        elif button_b.value() == 0:
            oled.fill(0)
            oled.show()
            break
        
        oled.show()

# 替换回文件（成功运行一次后，下一次换回文件）
# 当用户按下A，main.py 变为 main.py.main；main.py.bak 变为 main.py 系统重启
# 第一次重启时，将 main.py.main 变为 main.py.main_ 表示已经运行了备份的代码，并在下一次重启时换回代码
# 下一次重启，程序发现有 main.py.main_ 便将 main.py 变为 main.py.bak；将 main.py.main_ 变为 main.py
# 因为掌控板没有检查文件是否存在的功能，所以使用 try 语句来拦截报错。
try:  # 文件是否存在
    os.rename("main.py.main_", "main.py.main__")
    os.rename("main.py", "main.py.bak")
    os.rename("main.py.main__", "main.py")
except OSError:
    pass
try:  # 文件是否存在
    os.rename("main.py.main", "main.py.main_")
except OSError:
    pass
