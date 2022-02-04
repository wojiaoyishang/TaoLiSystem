# loader.py 最开始的加载者，用于整个系统的加载，
# 向无私奉献的加载者致敬！

# 导入 mpython 支持库
from mpython import *
import ntptime

import TaoLiSystem.config as config
import TaoLiSystem.wifi

def main(loadPluginFun):
    """任务安排员"""
    autoRunPlugin(loadPluginFun, True)
    wifiAutoConnect()
    dateAutoSet()
    autoRunPlugin(loadPluginFun)
    
def autoRunPlugin(loadPluginFun, beforeOther=False):
    """自动运行插件"""
    for filename in config.getAutoRunPlugin(beforeOther):
        with open("TaoLiSystem/plugin/" + filename) as f:
            c = f.read()
        loadPluginFun(c)
    
def wifiAutoConnect():
    """wifi自动连接"""
    if config.get('wifi', 'auto'):
        ssid = config.get('wifi', 'ssid')
        pwd = config.get('wifi', 'pwd')
        TaoLiSystem.wifi.connect(ssid, pwd)

def dateAutoSet():
    """时间自动设置"""
    if config.get('date', 'auto'):
        try:
            ntptime.settime()
        except:
            pass
        