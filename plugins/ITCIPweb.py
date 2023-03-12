# {"Name": "ITC网络数字广播","Version": "v0.0.1","Master": "以赏", "Description": "直接通过网络爬虫控制广播系统，前提是要连接到互联网。配置文件位于 TaoLiSystem/data/ITCIPweb 下。", "More": "由以赏制作"}
# 哈哈哈哈哈！鳌江中学的广播系统密码竟然这么简单！？

from mpython import *
import json
import time
import socket
import os

import TaoLiSystem.function

from TaoLiSystem.ItemSelector import ItemSelector as ItemSelector
from TaoLiSystem.morseType import MorseType as MorseType
from TaoLiSystem.TXTreader import TXTreader as TXTreader

config = {}


def http_get(url,headers=""):
    # 解析url
    _, _, host, path = url.split('/', 3)
    # 将网站的域名解析成IP地址
    addr = socket.getaddrinfo(host, 80)[0][-1]
    # 构建socket
    s = socket.socket()
    # 连接IP地址
    s.connect(addr)
    # 以http get 请求格式发送
    s.send((('GET /{path} HTTP/1.0\r\n' + \
            'Host: {host}\r\n' + \
            '{headers}' + \
            '\r\n\r\n').format(path=path, host=host, headers=headers)).encode('utf-8'))
    alldata = b''
    while True:
        # socket接收
        data = s.recv(100)
        if data:
            alldata += data

        else:
            break
    
    s.close()
    
    return alldata

def http_post(url,headers="",data=""):
    # 解析url
    _, _, host, path = url.split('/', 3)
    # 将网站的域名解析成IP地址
    addr = socket.getaddrinfo(host, 80)[0][-1]
    # 构建socket
    s = socket.socket()
    # 连接IP地址
    s.connect(addr)
    # 以http get 请求格式发送
    s.send((('POST /{path} HTTP/1.0\r\n' + \
            'Content-Length: {length}\r\n' + \
            'Host: {host}\r\n' + \
            '{headers}' + \
            '\r\n\r\n{data}').format(length=len(data), path=path, host=host, headers=headers,data=data)).encode('utf-8'))
    alldata = b''
    while True:
        # socket接收
        data = s.recv(100)
        if data:
            alldata += data

        else:
            break
    
    s.close()
    
    return alldata


try:
    # 查看是否存在 data 文件夹
    os.mkdir("TaoLiSystem/data")
except:
    pass
try:
    # 查看是否存在 IRlearn 文件夹
    os.mkdir("TaoLiSystem/data/ITCIPweb")
except:
    pass
try:
    with open("TaoLiSystem/data/ITCIPweb/config.json", "r") as f:
        config = json.loads(f.read())
except:
    pass

def go(ip="", user="", pwd=""):
    print(ip, user, pwd)
    if ip == "":
        ip = MorseType("输入 IP 地址").start()
        if ip == "":
            ip = "gb.lovepikachu.top"
        user = MorseType("输入 用户名").start()
        if user == "":
            user = "admin"
        pwd = MorseType("输入 密码").start()
        if pwd == "":
            pwd = "123456"
      
    print(ip, user, pwd)
    TaoLiSystem.function.waitingPage("正在", "登录", "OvO")
    oled.show()
    with open("TaoLiSystem/data/ITCIPweb/config.json", "w") as f:
        f.write(json.dumps({"ip":ip, "user":user, "pwd":pwd}))
    try:
        result = http_post("http://" + ip + "/Home/Login/sub_login", data="user={}&client_login=&pass={}".format(user, pwd),
                           headers="cookie: language=0\r\nContent-Type: application/x-www-form-urlencoded; charset=UTF-8\r\nX-Requested-With: XMLHttpRequest")
        result = result.decode()
        pos = result.find("Set-Cookie: PHPSESSID=") + len("Set-Cookie: ")
        cookie = result[pos:result.find(";", pos)]
        login_state = result[result.find("\r\n\r\n")+4:].strip()
        if login_state == "1":
            TaoLiSystem.function.waitingPage("登录", "成功", "惹！")
            oled.show()
            time.sleep(2)
            
            
            while True:
                action = ItemSelector(["会话管理"], "操作").start()
                if action == "":
                    break
                elif action == "会话管理":
                    TaoLiSystem.function.loadingPage("正在获取中......", 10, 5)
                    oled.show()
                    
                    result = http_get("http://" + ip + "/Home/Huihua/jsonindex",
                             headers="cookie: " + cookie).decode()
                    
                    result = result[result.find("\r\n\r\n")+4:].strip()
                    h = {}
                    if result != "error":
                        for x in json.loads(result)['so']:
                            h[x['js_task_name']] = x
                        
                    while True:
                        name = ItemSelector(list(h.keys()), "会话管理").start()
                        if name == "":
                            break
                        action = ItemSelector(["强制结束(!)", "详情"], "会话操作").start()
                        if action == "":
                            break
                        elif action == "详情":
                            if name in h:
                                TXTreader("懒地写了" + str(h[name]), "详情").start()
                            else:
                                break
                        elif action == "强制结束(!)":
                            if name in h:
                                result = http_get("http://" + ip + "/Home/Huihua/qzjs?ip=" + h[name]['js_task_hashkey'], headers="cookie: " + cookie).decode()
                                result = result[result.find("\r\n\r\n")+4:].strip()
                                if result == "1":
                                    TaoLiSystem.function.waitingPage("结束", "成功", "惹！")
                                    oled.show()
                                    time.sleep(2)
                                    break
                            else:
                                break
                    
            
        elif login_state == "5":
            TaoLiSystem.function.waitingPage("内部", "代码", "错误")
            oled.show()
            time.sleep(2)
        elif login_state == "7":
            TaoLiSystem.function.waitingPage("账号", "密码", "错误")
            oled.show()
            time.sleep(2)
        else:
            print(login_state)
    except:
        TaoLiSystem.function.waitingPage("连接", "失败", "！！")
        oled.show()
        time.sleep(2)

while True:
    action = ItemSelector(["按上次配置登录", "输入ITC信息"], "操作").start()
    
    if action == "":
        break
    elif action == "按上次配置登录":
        try:
            go(config['ip'], config['user'], config['pwd'])
        except  BaseException as error:
            print(str(error))
            pass
    elif action == "输入ITC信息":
        go()
        

        


