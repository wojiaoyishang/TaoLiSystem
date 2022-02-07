# plugin.py 啊啊啊啊啊，这是这个系统最后一个页面了。
# 因为插件分 本地插件 和 在线插件。插件的编写没什么好说的。
# 但是要设计一个插件格式来标识插件的名称、作者、介绍、版本等信息。
# 我打算用一种人类可读、机器有好识别的方式来标识。
# 插件格式具体看 tips.py 。
# 插件页面由 皮卡丘 和 Niko 赞助！
# 导入 mpython 支持库
from mpython import *
import urequests
import time
import json
import os

import TaoLiSystem.function
import TaoLiSystem.config as config
from TaoLiSystem.ItemSelector import ItemSelector as ItemSelector
from TaoLiSystem.TXTreader import TXTreader as TXTreader



class PluginPage():
    def __init__(self, loadPluginFunction):
        self.loadPluginFunction = loadPluginFunction
        print("看到这一段话说明插件页面已经成功被初始化！")
        return
    
    def show(self):
        """插件的主要页面"""
        while config.get_value("page") == 'plugin':
            item = ItemSelector(["本地插件", "在线插件"], "插件使用").start()
            
            if item == "":
                time.sleep_ms(500)
                config.set_value("page", "home")
                print("取消选择，回到主页")
                break
            
            while item == "本地插件":
                TaoLiSystem.function.waitingPage("加载", "插件", "中！")
                oled.show()
                
                pluginDict = {}
                for pluginFilename in self._getLocalPluginFilename():
                    info = self._getLocalPluginInfo(pluginFilename)
                    name = info.get("Name", None)
                    if name != None:
                         pluginDict[name] = info
                
                plugin = ItemSelector(list(pluginDict.keys()), "本地插件").start()
                if plugin == "":
                    break
                self.pluginManager(pluginDict[plugin])
                
            while item == "在线插件":
                TaoLiSystem.function.waitingPage("加载", "插件", "中！")
                oled.show()
                
                try:
                    result = urequests.get("http://119.91.220.81:5908/TLCSPlugins")
                    pluginDict = result.json()
                except BaseException as error:
                    print(str(error))
                    TaoLiSystem.function.waitingPage("加载", "失败", "QAQ")
                    oled.show()
                    time.sleep(1)
                    break
                
                plugin = ItemSelector(list(pluginDict.keys()), "在线插件").start()
                if plugin == "":
                    break
                self.pluginManager(pluginDict[plugin], False)
                    
                
            
    def pluginManager(self, pluginInfo, local=True):
        """插件管理"""
        # {"Name": "插件名称","Version": "v0.0.1","Master": "插件制作者","Description": "插件介绍", "More": "更多说明会直接附在插件页面后面"}
        while True:
            Name = pluginInfo['Name']
            Version = pluginInfo['Version']
            Master = pluginInfo['Master']
            Description = pluginInfo['Description']
            More = pluginInfo['More']
            Filename = pluginInfo['Filename']
            
            if local:
                item = ItemSelector(["加载插件", "查看详情", "删除插件"], Name).start()
            else:
                item = ItemSelector(["下载并运行插件", "仅下载插件", "查看详情"], Name).start()
            
            if item == "":
                break
            elif item == "查看详情":
                TaoLiSystem.function.waitingPage("正在", "加载", "...")
                oled.show()
                TXTreader("插件名称：%s\n插件版本：%s\n插件作者：%s\n插件简介：%s\n%s\n插件文件名：%s" % (Name, Version, Master, Description, More, Filename), "插件简介").start()
            elif item == "删除插件":
                item = ItemSelector(["不是不是，点错了", "是的，谢谢提醒"], "你真的要删除吗？").start()
                if item == "是的，谢谢提醒":
                    os.remove("TaoLiSystem/plugin/" + Filename)
                    TaoLiSystem.function.waitingPage("已经", "删除", "了哦")
                    oled.show()
                    time.sleep(1)
                    break
            elif item == "加载插件":
                self.loadPlugin(Filename)
            elif item == "仅下载插件":
                self._downloadPlugin(Filename)
            elif item == "下载并运行插件":
                self._downloadPlugin(Filename, True)
    
    def _downloadPlugin(self, url, load=False):
        """提供网址下载插件"""
        TaoLiSystem.function.waitingPage("下载", "插件", "中！")
        oled.show()
        
        try:
            Filename = url[url.rfind("/") + 1:]
            with open("TaoLiSystem/plugin/" + Filename, "wb") as f:
                f.write(urequests.get(url).content)
                
        except BaseException as error:
            print(str(error))
            TaoLiSystem.function.waitingPage("下载", "失败", "QAQ")
            oled.show()
            time.sleep(1)
            return
        
        TaoLiSystem.function.waitingPage("下载", "成功", "OvO")
        oled.show()
        time.sleep(1)
        if load:
            self.loadPlugin(Filename)
        return
    
    
        
    def _getLocalPluginInfo(self, PluginFileName):
        """通过文件名（要加拓展名）获取本地插件的插件原信息"""
        path = "TaoLiSystem/plugin/" + PluginFileName
        try:
            with open(path, "r") as f:
                r = f.readline().replace("#", "").strip()
            info  = json.loads(r)
            info['Filename'] = PluginFileName
            return info
        except:
            return {}
    
    def _getLocalPluginFilename(self):
        """获取本地插件的插件名称"""
        files = os.listdir("TaoLiSystem/plugin/")
        return list([file for file in files if file[file.rfind("."):] == ".py"])
    
    def loadPlugin(self, Filename, tip=True):
        """加载插件"""
        if tip:
            TaoLiSystem.function.waitingPage("正在", "加载", "...")
            oled.show()
            TXTreader("加载插件的说明\n由于插件功能仍然在内测，部分插件可能需要大量的内存，"
                      "在调用时可能会出现系统奔溃重启或者死机，部分插件没有设置退出开关，会使插件运行时无法退出（必须强制重启）。如果您信任该插件请继续。", "加载说明").start()
            if ItemSelector(["我再想想", "嗯，请继续"], "继续运行吗？").start() != "嗯，请继续":
                return

        exec_code = ""
        with open("TaoLiSystem/plugin/" + Filename, "r") as f:
            exec_code = f.read()

        
        self.loadPluginFunction(exec_code)
        return
    

