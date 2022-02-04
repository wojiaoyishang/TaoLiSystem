# setting.py 「...」
# 「你来了......」
# 「这只是一个设置页面」
# 「没什么好更改的」
# 「即便这样.....你还是想要查看下面的代码吗？」
# 「那么请记住」
# 「你的“任务”是帮助开发者修改BUG」

# 导入 mpython 支持库
from mpython import *
import ntptime

# 导入陶丽库中的模块
import TaoLiSystem.config as config
from TaoLiSystem.ItemSelector import ItemSelector as ItemSelector
from TaoLiSystem.TXTreader import TXTreader as TXTreader
from TaoLiSystem.morseType import MorseType as MorseType

import TaoLiSystem.wifi
import TaoLiSystem.function



class SettingPage():
    """设置页面"""
    def __init__(self):
        print("看到这一段话说明设置页面已经成功被初始化！")
        return
    
    def show(self):
        """设置界面显示入口"""
        while config.get_value("page") == 'setting':
            item = ItemSelector(["WIFI选项", "时间选项", "关于系统"], "系统选项").start()
            if item == "WIFI选项":
                WifiSetting().main()
            elif item == "时间选项":
                dateSetting().main()
            elif item == "关于系统":
                TXTreader("TaoLiSystem 系统简称 TLCS。由以赏制作，其取名灵感来源于我们高中的信息老师陶丽。系统特供给 Niko、皮卡丘、陶丽和林子琪同学！", "关于系统").start()
            else:
                time.sleep_ms(500)
                config.set_value("page", "home")
                print("退回 home")
                break
            

class dateSetting():
    """时间设置"""
    def __init__(self):
        print("初始化了 时间 设置")
        return
    
    def main(self):
        """时间设置主要大类"""
        while True:
            item = ItemSelector(["联机自动同步时间(%s)" %("√" if config.get('date', 'auto') else "×"), "马上同步时间"], "时间选项").start()
            if item == "":
                break
            elif item in ("联机自动同步时间(√)","联机自动同步时间(×)"):
                config.put('date', 'auto', not config.get('date', 'auto'))
            elif item == "马上同步时间":
                try:
                    ntptime.settime()
                except BaseException as error:
                    TaoLiSystem.function.loadingPage("同步时间出错惹......", 10, 5)
                    time.sleep(0.5)
                    oled.show()
                    TaoLiSystem.function.loadingPage(str(error), 0, 5)
                    time.sleep(0.5)
                    oled.show()
                TaoLiSystem.function.loadingPage("同步时间成功了哦！", 10, 5)
                oled.show()
                
            
    
    
class WifiSetting():
    """Wifi设置"""
    def __init__(self):
        print("初始化了 WIFI 设置")
        return
        
    def main(self):
        """WIFI设置主要大类"""
        while True:
            # 判断是否已经连接wifi
            if TaoLiSystem.wifi.is_connected():
                items = ["断开WIFI连接", "连接上次WIFI", "查看WIFI信息", "自动连接WIFI(%s)" % ("√" if config.get('wifi', 'auto') else "×")]
            else:
                items = ["启动扫描连接", "连接上次WIFI", "自动连接WIFI(%s)" % ("√" if config.get('wifi', 'auto') else "×")]
            item = ItemSelector(items, "WIFI选项").start()
            if item == "启动扫描连接":
                self.scanAndConnect()
            elif item == "连接上次WIFI":
                self.connectFileWifi()
            elif item in ("自动连接WIFI(√)", "自动连接WIFI(×)"):
                config.put('wifi', 'auto', not config.get('wifi', 'auto'))
            elif item == "查看WIFI信息":
                self.wifiInfo()
            elif item == "断开WIFI连接":
                TaoLiSystem.wifi.disconnect()
            else:
                break
    
    def scanAndConnect(self):
        """启动扫描连接"""
        while True:
            TaoLiSystem.function.loadingPage("正在扫描WIFI中......", 10, 5)
            oled.show()
            ssid = ItemSelector(["摩尔斯手动输入"] + TaoLiSystem.wifi.scan(), "扫描到的WIFI").start()
            if ssid == "":
                return
            elif ssid == "摩尔斯手动输入":
                ssid = MorseType().start()
            pwd = ItemSelector(["gqey3669", "a88888888", "12345678", "88888888", "摩尔斯手动输入"], "使用密码连接").start()
            if pwd == "":
                continue
            elif pwd == "摩尔斯手动输入":
                pwd = MorseType().start()
            self._connectWifi(ssid, pwd)
            break

    def connectFileWifi(self):
        """连接上次保存到文件里的wifi"""
        ssid = config.get('wifi', 'ssid')
        pwd = config.get('wifi', 'pwd')
        self._connectWifi(ssid, pwd)
            
    def _connectWifi(self, ssid, pwd):
        """连接wifi的过程"""
        TaoLiSystem.function.loadingPage("连接WIFI中，请稍等", 10, 5)
        oled.show()
        # 连接wifi
        if TaoLiSystem.wifi.connect(ssid, pwd):
            # 保存一下信息
            TaoLiSystem.config.put("wifi", "ssid", ssid)
            TaoLiSystem.config.put("wifi", "pwd", pwd)
            
            TaoLiSystem.function.loadingPage("连接WIFI成功了哦！", 10, 5)
            oled.show()
            time.sleep(0.5)
            TaoLiSystem.function.loadingPage("     已自动保存信息  ", 10, 5)
            oled.show()
            
            time.sleep(2)
            
            # 是否自动连接呢？
            auto = ItemSelector(["好啊好啊", "不用了，谢谢！"], "下次自动连接？").start()
            if auto == "好啊好啊":
                TaoLiSystem.config.put("wifi", "auto", True)
                
        else:
            TaoLiSystem.function.loadingPage("连接WIFI失败惹.....", 10, 5)
            oled.show()
            time.sleep(2)
    
    def wifiInfo(self):
        """wifi信息"""
        info = TaoLiSystem.wifi.info()
        content = "SSID:%s\nIP:%s\ngateway:%s\nsubnet_mask:%s\nDNS:%s"  % \
                  (config.get_value("wifiSSID"), info[0], info[1], info[2], info[3])
        TXTreader(content, "网络信息").start()
        