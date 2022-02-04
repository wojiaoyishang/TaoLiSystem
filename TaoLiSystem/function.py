# function.py 用于存储一些常用的函数。
# 此页面由 PIKACHU 提议。

# 导入 mpython 支持库
from mpython import *
from gui import Image

image = Image()

def loadingPage(text, x, y):
    """加载页面绘制"""
    oled.fill(1)
    i = image.load('TaoLiSystem/picture/loadingPage.bmp', 0)
    oled.blit(i, 0, -4)
    oled.DispChar(text, x, y, 2)
    del i

def waitingPage(text1, text2, text3):
    """加载页面绘制"""
    oled.fill(1)
    i = image.load('TaoLiSystem/picture/waitingPage.bmp', 0)
    oled.blit(i, 0, 0)
    oled.DispChar(text1, 98, 7, 2)
    oled.DispChar(text2, 98, 24, 2)
    oled.DispChar(text3, 98, 41, 2)
    del i