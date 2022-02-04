# {"Name": "插件名称","Version": "v0.0.1","Master": "插件制作者","Description": "插件介绍", "More": "更多说明会直接附在插件页面后面"}
from mpython import *
import time

oled.fill(0)
oled.DispChar('你好世界', 38, 0)
oled.DispChar('hello,world', 32, 16)
oled.DispChar('안녕하세요', 35, 32)
oled.DispChar('こんにちは世界', 24, 48)
oled.show()

time.sleep(10)