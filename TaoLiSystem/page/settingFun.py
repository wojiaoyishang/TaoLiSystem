# 系统各项小设置函数定义
# 2024.7.17 蓝牙内容的增加与修改感谢 罗米奇
# 2024.7.17 更新了主页选择
import os
import gc
import uio
import sys
import machine
import ubinascii
import time

from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

def connect_setting():
    selected_option_id = 0
    while True:
        selected_option_id = sysgui.itemSelector("无线网络选项", ["WIFI选项", "蓝牙选项"], selected_id=selected_option_id)
        
        if selected_option_id is None:
            return
        
        if selected_option_id == 0:
            wifi_setting()
        else:
            bluetooth_setting()

def enable_bluetooth():
    print("蓝牙开启前运存大小:", gc.mem_free())
    sysgui.tipBox("开启蓝牙中......", 0)
    if utils.enableBluetooth():
        global_var['bluetooth_BLE'] = True  # 启用蓝牙时设置键
    utils.enableBluetooth()
    sysgui.tipBox("蓝牙已启用", 1)
    print("蓝牙开启后运存大小:", gc.mem_free())
    
def disable_bluttooth():
    print("蓝牙关闭前运存大小:", gc.mem_free())
    sysgui.tipBox("关闭蓝牙中......", 0)
    utils.disableBluetooth()
    global_var.pop('bluetooth_BLE', None)  # 禁用蓝牙时安全地删除键
    sysgui.tipBox("蓝牙已关闭", 1)
    print("蓝牙关闭后运存大小:", gc.mem_free())

def bluetooth_setting():
    selected_option_id = 0
    while True:
        gc.collect()
        
        # 判断蓝牙是否开启
        bluetooth_options = []
        
        if 'bluetooth_BLE' not in global_var:
            bluetooth_options.append("(×)蓝牙状态")
        else:
            bluetooth_options.append("(√)蓝牙状态")
        
        bluetooth_options.append("设置蓝牙名称")
        bluetooth_options.append("查看蓝牙信息")
        
        selected_option_id = sysgui.itemSelector("蓝牙选项", bluetooth_options, selected_id=selected_option_id)
        
        if selected_option_id is None:
            return
        
        if bluetooth_options[selected_option_id] == "(×)蓝牙状态":    
            if utils.isEnableWIFI():
                if sysgui.messageBox("蓝牙和WIFI只能\n开启一个，继续？", yes_text="是的", no_text="取消"):
                    utils.disableWIFI()
                    enable_bluetooth()
                    continue
            else:
                enable_bluetooth()
                
        elif bluetooth_options[selected_option_id] == "(√)蓝牙状态":
            disable_bluttooth()
            if sysgui.messageBox("mPython代码限制\n必须重启哦。", yes_text="好", no_text="算了"):
                machine.reset()
        elif bluetooth_options[selected_option_id] == "设置蓝牙名称":
            if sysgui.messageBox("需要输入新的名称。"):
                name = sysgui.textTypeBox()
                configData.write("system", "bluetooth_name", name)
                sysgui.tipBox("修改成功！")
        elif bluetooth_options[selected_option_id] == "查看蓝牙信息": 
            bluetooth_name = configData.read("system", "bluetooth_name")
            bluetooth_address = ubinascii.hexlify(machine.unique_id()).decode().upper()
            formatted_address = ":".join([bluetooth_address[i:i+2] for i in range(0, len(bluetooth_address), 2)])
            if bluetooth_name is None or bluetooth_name.strip() == "":
                # 在这里处理bluetooth_name为空或全是空格的情况
                name = "mpython-HID"
                configData.write("system", "bluetooth_name", name)
                bluetooth_name = "（空）"   # 或者您可以设置默认的蓝牙名称
            sysgui.messageBox("蓝牙地址：\n" + formatted_address + "\n设备名称：" + bluetooth_name)
        
    
def wifi_setting():
    selected_option_id = 0
    
    while True:
        gc.collect()
        
        wifi_options = []
        
        # 判断 WIFI 是否开启
        if not utils.isEnableWIFI():
            wifi_options.append("(×)WIFI状态")
        else:
            wifi_options.append("(√)WIFI状态")
            if utils.isConnectWIFI():
                wifi_options.append("断开连接")
            else:
                wifi_options.append("扫描并连接")
                
            wifi_options.append("(×)自动连接" if not configData.read("system", "autoConnectWIFI") == "1" else "(√)自动连接")
        
        selected_option_id = sysgui.itemSelector("WIFI选项", wifi_options, selected_id=selected_option_id)
        
        if selected_option_id is None:
            return
        
        if wifi_options[selected_option_id] == "(×)WIFI状态":
            if utils.isEnableBluetooth():
                if sysgui.messageBox("WIFI和蓝牙只能\n开启一个，继续？", yes_text="是的", no_text="取消"):
                    if not sysgui.messageBox("mPython代码限制，\n会导致重启，继续？", yes_text="是的", no_text="取消"):
                        continue
                    utils.disableBluetooth()
                    # 开启无线
                    print("WIFI开启前运存大小:", gc.mem_free())
                    sysgui.tipBox("开启WIFI中......", 0)
                    utils.enableWIFI()
                    sysgui.tipBox("WIFI已启用", 1)
                    print("WIFI开启后运存大小:", gc.mem_free())
                    continue
            else:
                print("WIFI开启前运存大小:", gc.mem_free())
                sysgui.tipBox("开启WIFI中......", 0)
                utils.enableWIFI()
                sysgui.tipBox("WIFI已启用", 1)
                print("WIFI开启后运存大小:", gc.mem_free())
        elif wifi_options[selected_option_id] == "(√)WIFI状态":  # 扫描连接
            # 关闭无线
            print("WIFI关闭前运存大小:", gc.mem_free())
            sysgui.tipBox("关闭WIFI中......", 0)
            utils.disableWIFI()
            sysgui.tipBox("WIFI已禁用", 1)
            print("WIFI关闭后运存大小:", gc.mem_free())
        elif wifi_options[selected_option_id] == "扫描并连接":
            sysgui.tipBox("扫描 WIFI 中......", 0)
            available_networks = wifi().sta.scan()
            print("扫描到的WIFI：", available_networks)
            if len(available_networks) == 0:
                sysgui.tipBox("没有扫描到WIFI！\n请尝试重启WIFI服务", 0)
                continue 
            leave = False
            while not leave:
                selected_network_index = sysgui.selectionBox(
                    ["WIFI名称：%s\nRSSI：%d\n(%s)" % (w[0].decode()[:5] + "..." if len(w[0].decode()) > 5 else w[0].decode(),
                     w[3], ['开放', 'WEP', 'WPA_PSK', 'WPA_PSK', 'WPA_WPA2_PSK', 'MAX'][w[4]]) for w in available_networks])
                
                if selected_network_index is None:
                    leave = True
                    continue  # 回到 WIFI 设置
                
                operation_index = sysgui.itemSelector(available_networks[selected_network_index][0].decode()[:8] + "..."
                                                      if len(available_networks[selected_network_index][0].decode()) > 8
                                                      else available_networks[selected_network_index][0].decode(),
                                                      ["连接", "查看详情", "实时跟踪"])

                if operation_index is None:
                    continue  # 回到 WIFI 选择
                
                if operation_index == 0:  # 连接
                    wifi_password = None
                    if available_networks[selected_network_index][4] != 0:
                        sysgui.messageBox("请输入WIFI密码")
                        wifi_password = sysgui.textTypeBox()
                        
                    utils.enableWIFI()
                    wifi().sta.connect(available_networks[selected_network_index][0].decode(), wifi_password)
                    time_ = time.time()
                    while wifi().sta.status() == 1001:
                        if time.time() - time_ >= 10:
                            break
                        sysgui.tipBox("连接WIFI中(%ds)......" % int(time.time() - time_), 0)
                    
                    if time.time() - time_ >= 10:
                        sysgui.tipBox("连接超时！", 1)
                        continue
                    else:
                        status_message = {1000: "未连接", 1001: "正在连接", 202: "密码错误", 201: "接入点没有回复",
                                   1010: "WIFI连接成功", 203: "方式请求错误", 200: "连接超时", 204: "握手超时"}[wifi().sta.status()]
                        
                        sysgui.tipBox(status_message, 1)
                        
                        if wifi().sta.status() == 1010:
                            if sysgui.messageBox("下次是否自动连接？", yes_text="好啊~", no_text="不了~"):
                                configData.write("system", "autoConnectWIFI", "1")
                                configData.write("system", "autoConnectWIFI_ssid", available_networks[selected_network_index][0].decode())
                                configData.write("system", "autoConnectWIFI_password", wifi_password)
                            
                        break
                                        
                elif operation_index == 1:  # 查看详情
                    text_buffer = uio.StringIO("WIFI名称：" + available_networks[selected_network_index][0].decode() + "\n" +
                                               "WIFI强度RSSI：" + str(available_networks[selected_network_index][3]) + "\n" +
                                               "WIFI加密方式：" + ['开放', 'WEP', 'WPA_PSK', 'WPA_PSK', 'WPA_WPA2_PSK', 'MAX'][available_networks[selected_network_index][4]])
                    sysgui.txtStreamReader(text_buffer, "WIFI详情")
                    text_buffer.close()
                elif operation_index == 2:  # 实时跟踪
                    def draw_info(wifi_info):
                        oled.fill(0)
                        sysgui.draw_string_center(wifi_info[0].decode() + "\n" +
                                                    "信号强度RSSI：" + str(wifi_info[3])  + "\n<长按A退出>", 0, ex=True)
                        oled.show()
                    
                    # 实时扫描并跟踪
                    draw_info(available_networks[selected_network_index])
                    while True:
                        if button_a.value() == 0:
                            break
                        track_networks = wifi().sta.scan()
                        for network in track_networks:
                            if network[1] == available_networks[selected_network_index][1]:
                                draw_info(network)
        elif wifi_options[selected_option_id] == "断开连接":
            wifi().sta.disconnect()
            sysgui.tipBox("断开连接成功！", 1)
        elif wifi_options[selected_option_id] == "查看详情":
            ip, subnet, gateway, dns = wifi().sta.ifconfig()
            config_data = [ip, subnet, gateway, dns]
            config_data_descriptions = ["本机地址：" + ip, "电子掩码："+ subnet, "网关：" + gateway, "DNS服务器：" + dns]
            selected_config_id = sysgui.itemSelector("网络详情", config_data_descriptions)
            
            if sysgui.itemSelector("设置", ["查看", "设置"]):  # 设置
                sysgui.messageBox("请输入新值")
                new_value = sysgui.textTypeBox()
                config_data[selected_config_id] = new_value
                try:
                    wifi().sta.ifconfig(config_data)
                    sysgui.tipBox("设置成功！", 1)
                except:
                    sysgui.tipBox("值不正确！", 1)
            else:
                text_buffer = uio.StringIO(config_data_descriptions[selected_config_id])
                sysgui.txtStreamReader(text_buffer, "WIFI详情")
        elif wifi_options[selected_option_id] == "(×)自动连接":
            configData.write("system", "autoConnectWIFI", "1")
        elif wifi_options[selected_option_id] == "(√)自动连接":
            configData.write("system", "autoConnectWIFI", "0")

def date_setting():
    selected_option_id = 0
    
    rtc = machine.RTC()
    datetime = list(rtc.datetime())
    while True:
        gc.collect()
        selected_option = []
        selected_option.append("手动设置时间")
        selected_option.append("立刻同步时间")
        selected_option.append("(√)自动同步时间" if configData.read("system", "autoSyncTime") == "1" else "(×)自动同步时间")
        selected_option_id = sysgui.itemSelector("日期时间选项", selected_option, selected_id=selected_option_id)
        
        if selected_option_id is None:
            return
        
        if selected_option_id == 0:  # 手动设置时间
            
            while True:
                date_option = sysgui.itemSelector("选择时间进行设置", ["保存设置",
                                                             "年：" + str(datetime[0]),
                                                             "月：" + str(datetime[1]),
                                                             "日：" + str(datetime[2]),
                                                             "时：" + str(datetime[4]),
                                                             "分：" + str(datetime[5]),
                                                             "秒：" + str(datetime[6])])
                
                if date_option is None:
                    continue
                
                if date_option == 0:
                    rtc.datetime(datetime)
                    sysgui.tipBox("时间设置成功！", 1)
                    break
                else:
                    index_name = "年月日时分秒"[date_option - 1]
                    sysgui.messageBox("需要输入新的" + index_name + "。")
                    value = int(sysgui.textTypeBox(all_text=["0123456789"]))
                    # 重新映射时间，RTC时间和索引不同 Issue:I9KT1M 感谢 @FsdTS233
                    datetime[dict(zip("年月日时分秒", [0,1,2,4,5,6]))[index_name]] = value
                    
        elif selected_option_id == 1:  # 立刻同步时间
            if utils.isConnectWIFI():
                sysgui.messageBox("同步时间需要\n连接WIFI。")
                continue
            sysgui.tipBox("同步时间中......", 0)
            if utils.syncTime():
                sysgui.tipBox("同步时间成功！", 2)
            else:
                sysgui.tipBox("同步时间失败！", 2)
            
        elif selected_option_id == 2:  # 切换是否自动同步时间
            configData.write("system", "autoSyncTime", "0" if configData.read("system", "autoSyncTime") == "1" else "1")
 
def system_setting():
    global touchPad_sensitivity
    selected_option_id = 0

    while True:
        gc.collect()
        options = ["电源选项", "屏幕设置", "主页设置", "触摸设置", "关于此系统"]
        selected_id = sysgui.itemSelector("掌控板设置", options, selected_id=selected_option_id)
        
        if selected_id is None:
            break
        
        selected_option = options[selected_id]
        
        if selected_option == "电源选项":
            selected_id = sysgui.itemSelector("掌控板设置", ["硬重启", "软重启", "浅度睡眠", "深度睡眠"])
            if selected_id == 0:
                if sysgui.messageBox("确定硬重启？", yes_text="是的", no_text="稍后"):
                    machine.reset()
            elif selected_id == 1:
                if sysgui.messageBox("确定软重启？", yes_text="是的", no_text="稍后"):
                    machine.soft_reset()
            elif selected_id == 2:
                if sysgui.messageBox("确定进入浅度睡眠？\n按下 A 唤醒。", yes_text="是的", no_text="稍后"):
                    utils.lightsleep_irc()
            elif selected_id == 3:
                if sysgui.messageBox("确定进入深度睡眠？\n按下 A 唤醒。", yes_text="是的", no_text="稍后"):
                    utils.deepsleep_irc()  
        
        elif selected_option == "屏幕设置":  # 屏幕设置
            
            # 读取所有配置项 均读取为 str 类型
            ScreenOffStatus = configData.read("system", "ScreenOffStatus", "0")
            ScreenOffStatus_sleep = configData.read("system", "ScreenOffStatus_sleep", "0")
            ScreenOffTimeout = configData.read("system", "ScreenOffTimeout", "10")
            ScreenContrast = configData.read("system", "ScreenContrast", "255")
            
            while True:
                screen_setting = []
                screen_setting.append("屏幕亮度：" + ScreenContrast)
                screen_setting.append("(√)熄屏状态" if ScreenOffStatus == "1" else "(×)熄屏状态")
                screen_setting.append("熄屏时间：" + ScreenOffTimeout + "s")
                screen_setting.append("(√)熄屏进浅度睡眠" if ScreenOffStatus_sleep == "1" else "(×)熄屏进浅度睡眠")
                screen_setting.append("熄屏设置仅在首页有效")
                
                screen_setting_choice = sysgui.itemSelector("掌控板设置", screen_setting)
                
                if screen_setting_choice == 0:
                    sysgui.messageBox("需要输入屏幕亮度，\n最大255。")
                    value = sysgui.textTypeBox(all_text=["0123456789"])
                    if value.strip() == "" or value.strip() == " " or not value.isdigit():
                        sysgui.tipBox("输入不合法。")
                        continue
                        
                    configData.write("system", "ScreenContrast", min(int(value), 255))
                    ScreenContrast = str(min(int(value), 255))
                    oled.contrast(min(int(value), 255))
                    
                elif screen_setting_choice == 1:  # 熄屏状态
                    configData.write("system", "ScreenOffStatus", "0" if ScreenOffStatus == "1" else "1")
                    ScreenOffStatus = "0" if ScreenOffStatus == "1" else "1"
                    
                    # 顺便设置一下熄屏时间
                    configData.write("system", "ScreenOffTimeout", int(ScreenOffTimeout))
                    
                    if ScreenOffStatus == "1":
                        sysgui.messageBox("熄屏后，\n只能按下A唤醒。")  # 配合浅度睡眠
                elif screen_setting_choice == 2:
                    sysgui.messageBox("需要输入新熄屏时间\n为0则不启用熄屏。")
                    value = sysgui.textTypeBox(all_text=["0123456789"]).strip()
                    
                    # 乱输入的情况
                    if value == "" or not value.isdigit():
                        configData.write("system", "ScreenOffStatus", "0")  # 非法输入则拒绝，如果改配置文件强制设置，那就自作自受吧！
                        ScreenOffStatus = "0"
                        continue
                    
                    # 输入为零的情况
                    if value == "0":
                        configData.write("system", "ScreenOffStatus", "0")
                        configData.write("system", "ScreenOffTimeout", "10")
                        ScreenOffStatus = "0"
                    else:
                        configData.write("system", "ScreenOffTimeout", int(value))
                        ScreenOffTimeout = value
                        
                elif screen_setting_choice == 3:
                    sysgui.messageBox("睡眠可节约资源但\n部分硬件功能会暂停")
                    
                    configData.write("system", "ScreenOffStatus_sleep", "0" if ScreenOffStatus_sleep == "1" else "1")
                    ScreenOffStatus_sleep = "0" if ScreenOffStatus_sleep == "1" else "1"
                else:
                    break
                    
        elif selected_option == "主页设置":  # 主页设置
            homePage_setting()
            
        elif selected_option == "触摸设置":  # 触摸设置
            button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed  # 记录原先的按钮
            button_a.event_pressed, button_b.event_pressed = None, None
            while True:
                oled.fill(0)
                sysgui.draw_string_center("按下 P 测试触摸按键", 0)
                sysgui.draw_string_center("长按下 A+B 保存", 16)
                sysgui.draw_string_center("<A 阈值：%d B>" % touchPad_sensitivity, 32)
                sysgui.draw_string_center("检测阈值：%d %s" % (touchPad_P.read(), "未按下" if touchPad_P.read() > touchPad_sensitivity else "已按下"), 48)
                oled.show()
                
                if button_a.value() == 0 and button_b.value() == 0:
                    configData.write("system", "touchPad_sensitivity", str(touchPad_sensitivity))
                    button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
                    break
                elif button_a.value() == 0:
                    touchPad_sensitivity -= 10
                elif button_b.value() == 0:
                    touchPad_sensitivity += 10
            sysgui.tipBox("保存成功！")
            
        elif selected_option == "关于此系统":  # 关于
            try:
                f = open("./TaoLiSystem/COPYRIGHT", "r")
                sysgui.txtStreamReader(f, "关于此系统")
                f.close()
                def draw_qr():
                    __import__("gui").UI(oled).qr_code('https://gitee.com/wojiaoyishang/TaoLiSystem', 3, 3)
                    oled.DispChar("扫描查看", 70, 10)
                    oled.DispChar("开源仓库", 70, 26)
                    oled.DispChar("<A>", 85, 42)
                    oled.show()
                    del __import__("sys").modules['gui']
                sysgui.messageBox(None, content_fun=draw_qr)
                def draw_qr():
                    __import__("gui").UI(oled).qr_code('https://lovepikachu.top', 3, 3)
                    oled.DispChar("扫描查看", 70, 10)
                    oled.DispChar("皮卡丘哦", 70, 26)
                    oled.DispChar("<A>", 85, 42)
                    oled.show()
                    del __import__("sys").modules['gui']
                sysgui.messageBox(None, content_fun=draw_qr)
                sysgui.messageBox("谢谢各位的支持！", yes_text="不用谢")
            except OSError:
                sysgui.tipBox("版权文件不存在！", 1)
 

def homePage_setting():
    sysgui.messageBox("你将调整系统页面\n按下B保存更改")
    
    # 读取全部配置
    homePages = __import__('json').loads(configData.read('system', 'homePages', '["default"]'))
    page_id = int(configData.read('system', 'page_id', '1'))  # 默认页面 

    while True:
        print("当前界面顺序：", homePages)
        print("当前默认页面ID：", page_id)
        
        choices = []  # 选择对象

        for i, homePage in enumerate(["setting"] + homePages + ["plugin"]):
            if i == page_id:
                name = "首页\n" + homePage
            else:
                name = homePage
            
            if i in (0, len(homePages) + 1):  # 设置或者插件页面
                name += "\n系统界面"
            else:
                name += "\n自定义页面"
            
            choices.append(name)
        
        choice = sysgui.selectionBox(choices, selected_id=page_id)
        
        if choice is None:
            if sysgui.messageBox("保存并退出？", yes_text="是的", no_text="更多"):
                sysgui.tipBox("正在保存......", 0)
                
                # 写到配置文件
                configData.write('system', 'homePages',  __import__('json').dumps(homePages))
                configData.write('system', 'page_id',  page_id)
                
                # 同步主页
                from TaoLiSystem.core.loader import pages
                
                # 删掉所有
                for _ in range(len(pages)):
                    pages.pop()
                
                # 重新写入
                pages.append("TaoLiSystem.page.setting")
                for _ in homePages:
                    pages.append("TaoLiSystem.page.home." + _)
                pages.append("TaoLiSystem.page.plugin")
                
                break
            elif sysgui.messageBox("你要？", yes_text="放弃更改", no_text="继续修改", button_line=True):
                break
            else:
                continue
        
        while True:
            operates = []
            
            if choice == 0 or choice == len(choices) - 1:  # 设置或者插件页面
                operates.append("设为首页")
                operates.append("在前面插入页面")
                operates.append("在后面插入页面")
            else:
                operates.append("替换页面")
                operates.append("设为首页")
                operates.append("个性化设置")
                operates.append("删除")
                operates.append("在前面插入页面")
                operates.append("在后面插入页面")
            
            if choice == 0:
                operate = sysgui.itemSelector("ID:0 设置界面", operates)
            elif choice == len(homePages) + 1:
                operate = sysgui.itemSelector("ID:%d 插件界面" % (len(homePages) + 1), operates)
            else:
                operate = sysgui.itemSelector("ID:%d %s" % (choice, homePages[choice - 1]), operates)
            
            if operate is None:  # 没有选择
                break
            
            if operates[operate] == "替换页面":
                while True:
                    homes = [file for file in os.listdir("TaoLiSystem/page/home")]
                    home = sysgui.itemSelector("选择默认主页", homes)
                    
                    if home is None:
                        break
                    else:
                        homePages[choice - 1] = homes[home]  # homePages 与 choices 差 1
                        sysgui.messageBox("页面调整为:\n" + homes[home])
                        break
                    
            elif operates[operate] == "设为首页":
                page_id = choice
                sysgui.messageBox("页面设置为首页")
            
            elif operates[operate] == "个性化设置":
                sysgui.tipBox("加载中......")
                imported_modules = list(sys.modules.keys())
                print("TaoLiSystem.page.home." + homePages[choice - 1])
                setting = getattr(utils.importModule("TaoLiSystem.page.home." + homePages[choice - 1]), "setting")
                if setting:
                    setting()
                else:
                    sysgui.tipBox("这个主页没有个性化设置。")
                sysgui.tipBox("清理中......")
                utils.compare_and_clean_modules(imported_modules, [])
                
            elif operates[operate] == "删除":
                if sysgui.messageBox("确定删除\n" + "ID:%s %s" % (choice, homePages[choice - 1]) + "？", yes_text="是的", no_text="取消"):
                    del homePages[choice - 1]
                    if page_id == choice:  # 如果删除的是首页
                        page_id -= 1
                    break
                
            elif operates[operate] == "在前面插入页面":
                if choice == 0:  # 如果是设置
                    sysgui.messageBox("设置界面前面\n不允许插入页面")
                    continue
                while True:
                    homes = [file for file in os.listdir("TaoLiSystem/page/home")]
                    home = sysgui.itemSelector("选择插入的页面", homes)
                    
                    if home is None:
                        break
                    else:
                        homePages.insert(choice - 1, homes[home])
                        sysgui.messageBox("已插入页面:\n" + homes[home])
                        choice += 1  # 插入之后跟进
                        page_id += 1
                        break
                    
            elif operates[operate] == "在后面插入页面":
                if choice == len(homePages) + 1:  # 如果是设置
                    sysgui.messageBox("插件界面后面\n不允许插入页面")
                    continue
                while True:
                    homes = [file for file in os.listdir("TaoLiSystem/page/home")]
                    home = sysgui.itemSelector("选择插入的页面", homes)
                    
                    if home is None:
                        break
                    else:
                        homePages.insert(choice, homes[home])
                        sysgui.messageBox("已插入页面:\n" + homes[home])
                        choice -= 1  # 插入之后跟进
                        page_id -= 1
                        break
            
