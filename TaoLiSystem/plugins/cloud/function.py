import gc
import os
import uio
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

from TaoLiSystem.modules.ili934xnew import ILI9341, color565
from TaoLiSystem.modules import bmp_file_reader as bmpr
from machine import SPI
import urequests

pin_define = ["CS", "RST", "DC", "MOSI", "SCK"]
spi_pins = ["Pin.P16", "Pin.P15", "Pin.P14", "Pin.P20", "Pin.P13"]

for i in range(len(pin_define)):
    spi_pins[i] = configData.read("tft_pins", pin_define[i], spi_pins[i])
del i

def randpikachu():
    sysgui.tipBox("与 TFT 屏幕通讯......", 0)
    
    try:
        # 初始化 TFT
        spi = SPI(2, baudrate=20000000, mosi=Pin(eval(spi_pins[3])), sck=Pin(eval(spi_pins[4])))
        tft = ILI9341(spi, cs=Pin(eval(spi_pins[0])), dc=Pin(eval(spi_pins[2])), rst=Pin(eval(spi_pins[1])), w=320, h=240, r=0)
    except BaseException as e:
        gc.collect()
        
        if sysgui.messageBox("与 TFT 通讯出现错误！", yes_text="详情", no_text="返回"):
            f = uio.StringIO(str(e))
            sysgui.txtStreamReader(f, "报错")
            f.close()
        
        return
    gc.collect()
    
    try:
        tft.fill(0)
        tft.DispChar("与掌控板通讯中......", 0, 0, color565(255, 255, 255), buffer_char_line=1, buffer_width=None)
        
        # 请求服务器
        sysgui.tipBox("正在与服务器通讯......", 0)
        r = urequests.get("http://lab.lovepikachu.top/api/randpika?format=bmp&resize_width=240")
        response_json = r.json()
        r.close()
        if response_json['success'] == False:
            sysgui.tipBox("服务器拒绝请求!\n" + str(response_json['msg']))
            spi.deinit()
            del tft, spi
            return
        
        picture_url = response_json['data']
        del response_json
        
        sysgui.tipBox("正在保存图片......", 0)
        
        r = urequests.get(picture_url)
        f = open("temp.bmp", "wb+")
        
        c = r.recv(1024)
        
        while c:
            f.write(c)
            c = r.recv(1024)     
        del c
        
        r.close()
        gc.collect()
        sysgui.tipBox("正在显示图片......", 0)
        
        tft.refresh()
        #tft.fill(0)
        #tft.DispChar("皮卡丘插画：", 0, 0, color565(255, 255, 255), buffer_char_line=1, buffer_width=None)

        f.seek(0)
        gc.collect()
        tft.DispBmp(bmpr.BMPFileReader(f), 0, 0, 16)
        f.close()
        spi.deinit()
        del tft, spi
        
        sysgui.messageBox("完成！按下 A 退出！")
            
        sysgui.tipBox("正在清理临时文件......", 0)
        os.remove("temp.bmp")
    except BaseException as e:
        gc.collect()
        
        if sysgui.messageBox("出现错误了......", yes_text="详情", no_text="返回"):
            f = uio.StringIO(str(e))
            sysgui.txtStreamReader(f, "报错")
            f.close()
            
        spi.deinit()
    
def tft_pin_setting():
    selected_id = 0
    while True:
        selected_id = sysgui.itemSelector("选择修改的引脚", [pin_define[i] + ":" + spi_pins[i] for i in range(len(pin_define))])
        
        if selected_id is None:
            break
        
        sysgui.messageBox("需要输入新的 " + pin_define[i] + "。")
        
        value = sysgui.textTypeBox(spi_pins[i])
        
        sysgui.tipBox("正在保存......", 0)
        
        spi_pins[i] = value
        
        configData.write("tft_pins", pin_define[i], value)
        
        sysgui.tipBox("保存成功。", 1)
        
def randHorrorStory():
    gc.collect()
    # 请求服务器
    sysgui.tipBox("正在与服务器通讯......", 0)
    r = urequests.get("http://lab.lovepikachu.top/api/randpika?format=bmp&resize_width=240")
    response_json = r.json()
    r.close()
    if response_json['success'] == False:
        sysgui.tipBox("服务器拒绝请求!\n" + str(response_json['msg']))
        spi.deinit()
        del tft, spi
        return
    
    gc.collect()
    
    f = uio.StringIO(response_json["data"]["content"])
    del response_json
    sysgui.txtStreamReader(f, "随机鬼故事")
    f.close()
    
    
