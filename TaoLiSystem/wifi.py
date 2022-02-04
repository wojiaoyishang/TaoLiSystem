# wifi.py 集成了控制wifi所使用的命令
# 此页面由 陶丽 监制。
# 导入 mpython 支持库
from mpython import *
import TaoLiSystem.config as config

# 初始化一个wifi类
wifi = wifi()
wlan = network.WLAN(network.STA_IF)

def is_connected():
    """wifi是否连接"""
    return wifi.sta.isconnected()

def scan():
    """扫描wifi"""
    wlan.active(True)
    y = wlan.scan()
    wlan.active(False)
    return list([x[0].decode() for x in y])

def connect(ssid, pwd):
    """连接wifi 会把成功连接的WIFI ssid放入 全局 wifiSSID 变量中"""
    try:
        wifi.connectWiFi(ssid, pwd, 10)
    except:
        return False
    config.set_value("wifiSSID", ssid)
    return wifi.sta.isconnected()
def disconnect():
    """断开网络连接"""
    try:
        wifi.disconnectWiFi()
        return True
    except:
        return False

def info():
    """wifi的连接信息"""
    return wlan.ifconfig()