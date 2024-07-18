import time

from .mpython_ble.application import HID
from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

# 常量
KeyboardCode = {
    'A': 0x04,
    'B': 0x05,
    'C': 0x06,
    'D': 0x07,
    'E': 0x08,
    'F': 0x09,
    'G': 0x0A,
    'H': 0x0B,
    'I': 0x0C,
    'J': 0x0D,
    'K': 0x0E,
    'L': 0x0F,
    'M': 0x10,
    'N': 0x11,
    'O': 0x12,
    'P': 0x13,
    'Q': 0x14,
    'R': 0x15,
    'S': 0x16,
    'T': 0x17,
    'U': 0x18,
    'V': 0x19,
    'W': 0x1A,
    'X': 0x1B,
    'Y': 0x1C,
    'Z': 0x1D,
    '1': 0x1E,
    '2': 0x1F,
    '3': 0x20,
    '4': 0x21,
    '5': 0x22,
    '6': 0x23,
    '7': 0x24,
    '8': 0x25,
    '9': 0x26,
    '0': 0x27,
    'F1': 0x3A,
    'F2': 0x3B,
    'F3': 0x3C,
    'F4': 0x3D,
    'F5': 0x3E,
    'F6': 0x3F,
    'F7': 0x40,
    'F8': 0x41,
    'F9': 0x42,
    'F10': 0x43,
    'F11': 0x44,
    'F12': 0x45,
    ' ': 0x2C
}

NOUSE_KeyboardCode = {
    'ENTER': 0x28,
    'ESCAPE': 0x29,
    'BACKSPACE': 0x2A,
    'TAB': 0x2B,
    'SPACEBAR': 0x2C,
    'MINUS': 0x2D,
    'EQUALS': 0x2E,
    'LEFT_BRACKET': 0x2F,
    'RIGHT_BRACKET': 0x30,
    'BACKSLASH': 0x31,
    'POUND': 0x32,
    'SEMICOLON': 0x33,
    'QUOTE': 0x34,
    'GRAVE_ACCENT': 0x35,
    'COMMA': 0x36,
    'PERIOD': 0x37,
    'FORWARD_SLASH': 0x38,
    'CAPS_LOCK': 0x39,
    'PRINT_SCREEN': 0x46,
    'SCROLL_LOCK': 0x47,
    'PAUSE': 0x48,
    'INSERT': 0x49,
    'HOME': 0x4A,
    'PAGE_UP': 0x4B,
    'DELETE': 0x4C,
    'END': 0x4D,
    'PAGE_DOWN': 0x4E,
    'KEYPAD_NUMLOCK': 0x53,
    'KEYPAD_FORWARD_SLASH': 0x54,
    'KEYPAD_ASTERISK': 0x55,
    'KEYPAD_MINUS': 0x56,
    'KEYPAD_PLUS': 0x57,
    'KEYPAD_ENTER': 0x58,
    'KEYPAD_ONE': 0x59,
    'KEYPAD_TWO': 0x5A,
    'KEYPAD_THREE': 0x5B,
    'KEYPAD_FOUR': 0x5C,
    'KEYPAD_FIVE': 0x5D,
    'KEYPAD_SIX': 0x5E,
    'KEYPAD_SEVEN': 0x5F,
    'KEYPAD_EIGHT': 0x60,
    'KEYPAD_NINE': 0x61,
    'KEYPAD_ZERO': 0x62,
    'KEYPAD_PERIOD': 0x63,
    'KEYPAD_BACKSLASH': 0x64,
    'KEYPAD_EQUALS': 0x67,
    'F13': 0x68,
    'F14': 0x69,
    'F15': 0x6A,
    'F16': 0x6B,
    'F17': 0x6C,
    'F18': 0x6D,
    'F19': 0x6E,
    'LEFT_CONTROL': 0xE0,
    'CONTROL': 0xE0,  # Alias for LEFT_CONTROL
    'LEFT_SHIFT': 0xE1,
    'SHIFT': 0xE1,    # Alias for LEFT_SHIFT
    'LEFT_ALT': 0xE2,
    'ALT': 0xE2,      # Alias for LEFT_ALT
    'OPTION': 0xE2,   # Labeled as Option on some Mac keyboards
    'LEFT_GUI': 0xE3,
    'RIGHT_CONTROL': 0xE4,
    'RIGHT_SHIFT': 0xE5,
    'RIGHT_ALT': 0xE6,
    'RIGHT_GUI': 0xE7
}



# 读取配置
HID_NAME = configData.read("system", "bluetooth_name", "mPython-HID")  # HID_名字

# 变量
advertise_toggle = True
function_mode = False
control_tip = ""
exit_loop = False

if utils.isEnableWIFI():
    if not sysgui.messageBox("继续将会禁用WIFI。", yes="好的", no="算了"):
        raise ValueError("用户终止执行。")

if not utils.isEnableBluetooth():
    utils.enableBluetooth()

sysgui.tipBox("正在启动蓝牙HID......", 0)

# 创建对象
HID_remote = HID(name=HID_NAME.encode())
# 启动广播
HID_remote.advertise(toggle=advertise_toggle)

# 键盘输入回调
def keyboard_input_callback(origin_text, input_text, pos):
    global KeyboardCode, HID_remote
    if len(input_text) != 1:
        HID_remote.keyboard_send(KeyboardCode[input_text])
        return
    if input_text.isupper():
        HID_remote.keyboard_press(0xE1)
    HID_remote.keyboard_send(KeyboardCode[input_text.upper()])
    if input_text.isupper():
        HID_remote.keyboard_release(0xE1)
    return "", 0

while not exit_loop:
    oled.fill(0)
    sysgui.draw_rect_empty(0, 0, 128, 64)
    if not function_mode:
        sysgui.draw_string_center("<A 功能> <B 退出>", 1)
        sysgui.draw_string_center("鼠标模式", 16)
        sysgui.draw_string_center("<O 左键> <N 右键>", 32)
        sysgui.draw_string_center("<PYTH ↑←↓→>", 47)
    else:
        sysgui.draw_string_center("<A 功能> <B 断开>" if len(HID_remote.hid_device.connections) != 0 else ("<A 功能> <B 停播>" if advertise_toggle else "<A 功能> <B 起播>"), 1)
        sysgui.draw_string_center("键盘模式", 16)
        sysgui.draw_string_center("<O 字符> <N 更多>", 32)
        sysgui.draw_string_center("<PYTH ↑←↓→>", 47)
    
    oled.show()
    # 等待用户事件
    time_recoder = time.time()
    touchPad_O_pressed = False
    touchPad_N_pressed = False
    exit_loop2 = False
    while not exit_loop2:
        control_tip = ""
        
        if button_a.value() == 0:
            function_mode = not function_mode
            break
        elif not function_mode and button_b.value() == 0:
            # 退出
            HID_remote.disconnect()  # 断开连接
            HID_remote.advertise(toggle=False)
            HID_remote.hid_device.ble.active(False)
            del HID_remote.hid_device.ble
            exit_loop = True
            break
        elif function_mode and button_b.value() == 0:
            # 退出
            if len(HID_remote.hid_device.connections) != 0:
                HID_remote.disconnect()  # 断开连接
            else:
                advertise_toggle = not advertise_toggle
                HID_remote.advertise(toggle=advertise_toggle)
            break
        elif not function_mode and touchPad_P.read() <= touchPad_sensitivity:
            HID_remote.mouse_move(x=0, y=-5, wheel=0)
            control_tip = "↑"
        elif not function_mode and touchPad_Y.read() <= touchPad_sensitivity:
            HID_remote.mouse_move(x=-5, y=0, wheel=0)
            control_tip = "←"
        elif not function_mode and touchPad_T.read() <= touchPad_sensitivity:
            HID_remote.mouse_move(x=0, y=5, wheel=0)
            control_tip = "↓"
        elif not function_mode and touchPad_H.read() <= touchPad_sensitivity:
            HID_remote.mouse_move(x=5, y=0, wheel=0)
            control_tip = "→"
        
        if not function_mode and not touchPad_O_pressed and touchPad_O.read() <= touchPad_sensitivity:
            time_recoder = time.time()
            HID_remote.mouse_press(1)
            touchPad_O_pressed = True
        elif not function_mode and touchPad_O_pressed and touchPad_O.read() > touchPad_sensitivity:
            time_recoder = time.time()
            HID_remote.mouse_release(1)
            touchPad_O_pressed = False
        elif not function_mode and touchPad_N_pressed and touchPad_N.read() > touchPad_sensitivity:
            time_recoder = time.time()
            HID_remote.mouse_release(2)
            touchPad_O_pressed = False
        elif not function_mode and touchPad_N_pressed and touchPad_N.read() > touchPad_sensitivity:
            time_recoder = time.time()
            HID_remote.mouse_release(2)
            touchPad_O_pressed = False
            
        elif function_mode and touchPad_O.read() <= touchPad_sensitivity:  # 字符输入
            sysgui.textTypeBox(input_callback=keyboard_input_callback, all_text=["0123456789", "abcdef", "ghijkl", "mnopqr", "stuvwx", "yz", ["F1", "F2", "F3", "F4"],
                                                                                 ["F5", "F6", "F7", "F8"],
                                                                                 ["F9", "F10", "F11", "F12"]])
        elif function_mode and touchPad_N.read() <= touchPad_sensitivity:
            key_id = 0
            key_list = list(NOUSE_KeyboardCode.keys())
            while True:
                key_id = sysgui.itemSelector("未使用按键发送", key_list, key_id)
                
                if key_id is None:
                    exit_loop2 = True
                    break
                
                mode_id = sysgui.itemSelector("模式", ["点击", "按下", "松开", "松开全部"])
                
                if mode_id is None:
                    continue
                
                if mode_id == 0:
                    HID_remote.keyboard_send(NOUSE_KeyboardCode[key_list[key_id]])
                elif mode_id == 1:
                    HID_remote.keyboard_press(NOUSE_KeyboardCode[key_list[key_id]])
                elif mode_id == 2:
                    HID_remote.keyboard_release(NOUSE_KeyboardCode[key_list[key_id]])
                elif mode_id == 3:
                    HID_remote.keyboard_release_all()
        
        elif function_mode and touchPad_P.read() <= touchPad_sensitivity:
            HID_remote.keyboard_send(0x52)
            control_tip = "↑"
        elif function_mode and touchPad_Y.read() <= touchPad_sensitivity:
            HID_remote.keyboard_send(0x50)
            control_tip = "←"
        elif function_mode and touchPad_T.read() <= touchPad_sensitivity:
            HID_remote.keyboard_send(0x51)
            control_tip = "↓"
        elif function_mode and touchPad_H.read() <= touchPad_sensitivity:
            HID_remote.keyboard_send(0x4F)
            control_tip = "→"
            
        if control_tip:
            oled.fill(0)
            oled.DispChar(control_tip, 56, 64 // 2 - 16 //2)
            oled.show()
            time_recoder = time.time()
        
        if time.time() - time_recoder >= 3:
            break
        
    oled.show()
    

