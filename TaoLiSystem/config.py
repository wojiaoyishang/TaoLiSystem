# 此文件用于读取和写入配置文件，是对配置文件的操作。也用于不同模块间的变量传递。
# 我就是普通写个系统，没想到要考虑这么多东西......
# 你知道吗？上次玩完《OneShot》，真的......太感人了......
import json, os

globalDict = {}

def set_value(key, value):
    """设置全局变量"""
    globalDict[key] = value
    
def get_value(key):
    """获得全局变量"""
    return globalDict.get(key, None)

def get(key, child):
    """获取配置文件项目"""
    try:
        with open("TaoLiSystem/config.json", "r") as f:
            c = f.read()
            if c == "":
                c = "{}"
            return json.loads(c).get(key, {}).get(child, None)
    except OSError:
        return "" 

def put(key, child, value):
    """更改配置文件项目"""
    try:
        with open("TaoLiSystem/config.json", "r") as f:
            c = f.read()
            if c == "":
                c = "{}"
            s = json.loads(c)
            if key not in s:
                s[key] = {}
            s[key][child] = value
        with open("TaoLiSystem/config.json", "w") as f:
            f.write(json.dumps(s))
        return True
    except OSError: 
        return False

def addAutoRun(PluginFilename, beforeOther=False):
    """增加自启动项目 要加后缀名 beforOther=在wifi连接等之前"""
    try:
        if not beforeOther:
            autoRunPluginFilename = get("autoRun", "afterOther")
            if type(autoRunPluginFilename) != list:
                autoRunPluginFilename = []
            if PluginFilename not in autoRunPluginFilename:
                autoRunPluginFilename.append(PluginFilename)
                put("autoRun", "afterOther", autoRunPluginFilename)
        else:
            autoRunPluginFilename = get("autoRun", "beforeOther")
            if type(autoRunPluginFilename) != list:
                autoRunPluginFilename = []
            if PluginFilename not in autoRunPluginFilename:
                autoRunPluginFilename.append(PluginFilename)
                put("autoRun", "beforeOther", autoRunPluginFilename)
        return True
    except:
        return False
    
    
def removeAutoRun(PluginFilename, beforeOther=False):
    """删除自启动项目 要加后缀名 beforOther=在wifi连接等之前"""
    try:
        if not beforeOther:
            autoRunPluginFilename = get("autoRun", "afterOther")
            if type(autoRunPluginFilename) != list:
                autoRunPluginFilename = []
            if PluginFilename in autoRunPluginFilename:
                autoRunPluginFilename.remove(PluginFilename)
                put("autoRun", "afterOther", autoRunPluginFilename)
        else:
            autoRunPluginFilename = get("autoRun", "beforeOther")
            if type(autoRunPluginFilename) != list:
                autoRunPluginFilename = []
            if PluginFilename in autoRunPluginFilename:
                autoRunPluginFilename.remove(PluginFilename)
                put("autoRun", "beforeOther", autoRunPluginFilename)
        return True
    except:
        return False

def getAutoRunPlugin(beforeOther=False):
    """获取自启动插件 要加后缀名"""
    if not beforeOther:
        autoRunPluginFilename = get("autoRun", "afterOther")
        return autoRunPluginFilename if type(autoRunPluginFilename) == list else []
    else:
        autoRunPluginFilename = get("autoRun", "beforeOther")
        return autoRunPluginFilename if type(autoRunPluginFilename) == list else []
