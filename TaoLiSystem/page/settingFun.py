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

        # 判断 WIFI 是否开启
        if not utils.isEnableWIFI():
            wifi_options = ["(×)WIFI状态"]
        else:
            if utils.isConnectWIFI():
                wifi_options = ["(√)WIFI状态", "断开连接",
                           "(×)自动连接" if not configData.read("system", "autoConnectWIFI") == "1" else "(√)自动连接",
                           "查看详情"]
            else:
                wifi_options = ["(√)WIFI状态",
                           "(×)自动连接" if not configData.read("system", "autoConnectWIFI") == "1" else "(√)自动连接",
                           "扫描并连接"]
        
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
                selected_network_index = sysgui.selectionBox(["WIFI名称：%s\nRSSI：%d\n(%s)" % (w[0].decode()[:5] + "..." if len(w[0].decode()) > 5 else w[0].decode(),
                                                                  w[3],
                                                                  ['开放', 'WEP', 'WPA_PSK', 'WPA_PSK', 'WPA_WPA2_PSK', 'MAX'][w[4]])
                                    for w in available_networks])
                
                if selected_network_index is None:
                    leave = True
                    continue  # 回到 WIFI 设置
                
                operation_index = sysgui.itemSelector(available_networks[selected_network_index][0].decode()[:8] + "..." if len(available_networks[selected_network_index][0].decode()) > 8 else available_networks[selected_network_index][0].decode(),
                                                    ["连接", "查看详情", "实时跟踪"])

                if operation_index is None:
                    continue  # 回到 WIFI 选择
                
                if operation_index == 0:  # 连接
                    wifi_password = None
                    if available_networks[selected_network_index][4] != 0:
                        sysgui.messageBox("请输入WIFI密码")
                        wifi_password = sysgui.textTypeBox()
                    
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
        selected_option_id = sysgui.itemSelector("日期时间选项", ["手动设置时间", "立刻同步时间",
                                                            "(√)自动同步时间" if configData.read("system", "autoSyncTime") == "1" else "(×)自动同步时间"],
                                                 selected_id=selected_option_id)
        
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
            if "wifi" not in global_var or not global_var.get("wifi").sta.isconnected():
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
        selected_option_id = sysgui.itemSelector("掌控板设置", ["熄屏设置", "主页设置", "触摸设置", "关于此系统"],
                                                 selected_id=selected_option_id)
        
        if selected_option_id is None:
            return
        
        if selected_option_id == 0:  # 熄屏设置
            
            timeout = configData.read("system", "ScreenOffTimeout")
            if timeout is None:
                configData.write("system", "ScreenOffTimeout", "10")
                timeout = "10"
            
            sysgui.messageBox("熄屏后，\n按下A或B唤醒。")
            
            while True:
                screen_setting_choice = sysgui.itemSelector("掌控板设置", ["(√)熄屏状态" if configData.read("system", "ScreenOffStatus") == "1" else "(×)熄屏状态"
                                                                      , "熄屏时间：" + timeout + "s", "熄屏设置仅在首页有效"])
                
                if screen_setting_choice is None:
                    break
                
                if screen_setting_choice == 0:
                    configData.write("system", "ScreenOffStatus", "0" if configData.read("system", "ScreenOffStatus") == "1" else "1")
                elif screen_setting_choice == 1:
                    sysgui.messageBox("需要输入新熄屏时间\n为0则不启用熄屏。")
                    value = sysgui.textTypeBox(all_text=["0123456789"])
                    if value.strip() == "" or value.strip() == " ":
                        configData.write("system", "ScreenOffStatus", "0")  # 非法输入则拒绝，如果改配置文件强制设置，那就自作自受吧！
                    configData.write("system", "ScreenOffTimeout", value)
                    timeout = value
        elif selected_option_id == 1:  # 主页设置
            while True:
                home = configData.read("system", "homePage", "default")
                home_setting_choice = sysgui.itemSelector("主页设置", ["默认主页:" + home, "个性化设置"])
                
                if home_setting_choice == 0:  # 选择主页
                    homes = [file for file in os.listdir("TaoLiSystem/page/home")]
                    home = homes[sysgui.itemSelector("选择默认主页", homes)]
                    configData.write("system", "homePage", home)
                    if sysgui.messageBox("设置成功，\n是否立刻重启？", yes_text="是的", no_text="稍后"):
                        machine.reset()
                elif home_setting_choice == 1:  # 主页设置
                    sysgui.tipBox("加载中......")
                    imported_modules = list(sys.modules.keys())
                    setting = getattr(utils.importModule("TaoLiSystem.page.home." + home), "setting")
                    if setting:
                        setting()
                    else:
                        sysgui.tipBox("这个主页没有设置。")
                    sysgui.tipBox("清理中......")
                    utils.compare_and_clean_modules(imported_modules)
                else:
                    break

            
        elif selected_option_id == 2:  # 触摸设置
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
        elif selected_option_id == 2:  # 关于
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
 
