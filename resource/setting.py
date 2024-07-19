import os
import re
import sys
import ctypes
import operator
import traceback

# 配置项对应的说明
instructions = {
    "system:settingTipped": "设置页面新手提示",
    "system:homeTipped": "设置页面新手提示",
    "system:ScreenOffTimeout": "屏幕熄屏时间",
    "system:touchPad_sensitivity": "触摸按键敏感度",
    "system:ScreenOffStatus": "屏幕是否启用熄屏",
    "system:itemSelectorTipped": "选择器新手提示",
    "system:ScreenOffStatus_sleep": "是否启用熄屏浅睡眠",
    "system:autoConnectWIFI": "是否自动连接WIFI",
    "system:autoConnectWIFI_password": "自动连接WIFI密码",
    "system:autoConnectWIFI_ssid": "自动连接WIFI名称",
    "system:autoSyncTime": "是否自动同步时间",
    "FlappyBird:score": "插件飞行小鸟的最高分数",
    "weather:location": "天气插件的天气获取位置"
}

root = __file__.replace("\\", "/")

# 文件所在目录
build_file_path = root[:root.rfind("/")]
os.environ['PATH'] = build_file_path + os.pathsep + os.environ.get('PATH', '')
# 导入文件当前目录包，这样做是为了防止程序不在 resource 下运行时出现问题
__import__("requirements_check")  # 检测依赖
pyboard = __import__("pyboard");
pyboard_utils = __import__("pyboard_utils")
serial_ports = __import__('serial.tools.list_ports').tools.list_ports.comports()
if len(serial_ports) != 0:
    serial_port = serial_ports[0].device
else:
    serial_port = ""

# 系统预编译根目录
root = build_file_path[:build_file_path.rfind("/")]

# 掌控板配置文件位置
config_path = "TaoLiSystem/data/config.db"

# 是否在 Python 的 IDLE 中打开，就去掉 ESC 换行符
if any('idlelib' in mod for mod in sys.modules):
    _print = print


    def print(*args, **kwargs):
        clean_args = []
        for arg in args:
            if isinstance(arg, str):
                # 使用正则表达式移除所有 ANSI 转义序列
                clean_str = re.sub(r'\x1b\[[0-9;]*[mGKH]', '', arg)
                clean_args.append(clean_str)
            else:
                clean_args.append(arg)
        _print(*clean_args, **kwargs)


    _input = input


    def input(*args, **kwargs):
        clean_args = []
        for arg in args:
            if isinstance(arg, str):
                # 使用正则表达式移除所有 ANSI 转义序列
                clean_str = re.sub(r'\x1b\[[0-9;]*[mGKH]', '', arg)
                clean_args.append(clean_str)
            else:
                clean_args.append(arg)
        return _input(*clean_args, **kwargs)

# 开启 Windows 下对于 ESC控制符 的支持
if sys.platform == "win32":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

pre_cmd = """
import os
import btree

class Config:
    def __init__(self, filename='TaoLiSystem/data/config.db'):
        self.filename = filename
        self.db = self._open_db()

    def _open_db(self):
        try:
            f = open(self.filename, 'r+b')
        except OSError:
            f = open(self.filename, 'w+b')
        return btree.open(f)     

    def read(self, section, key, default=None):
        try:
            value = self.db[(section + ':' + key).encode()]
            return value.decode()
        except KeyError:
            return default
    
    def write(self, section, key, value):
        self.db[(section + ':' + key).encode()] = str(value).encode()
        self.db.flush()

    def close(self):
        self.db.close()


try: os.mkdir('TaoLiSystem/data')
except: pass

configData = Config()
"""


def is_chinese(uchar):
    # 判断当前字符是否为中文字符
    return uchar >= u'\u4e00' and uchar <= u'\u9fa5'


# 来自 https://blog.csdn.net/m0_73666951/article/details/135779470
def format_text(ustring):
    # 输入一个字符串，输出一个字符串
    # 输出字符串的显示宽度为指定宽度（非域宽）
    width = 20 * 3
    # 将20改为你想要的显示宽度（默认全角）
    # 注意显示宽度应当大于字符串中字符个数
    for uchar in ustring:
        width -= 3 if is_chinese(uchar) else 2
    return ustring + ' ' * int(width / 2) if width % 2 == 0 else ustring + '\u3000' + ' ' * int((width - 3) / 2)


def command_help():
    print("* 命令说明：")
    print(f"* set [设置项名称]=[设置项设定值] \t{format_text('更改设置项状态')}")
    print(f"* del [设置项名称] \t{format_text('删除设置项')}")
    print(f"* export \t{format_text('备份设置项到电脑')}")
    print(f"* import \t{format_text('从电脑恢复设置项')}")
    print(f"* show \t{format_text('展示所有配置项')}")
    print(f"* help \t{format_text('查看帮助')}")
    print(f"* bye \t{format_text('重启掌控板，退出程序')}")


def command_show(pyb):
    # 获取全部设置项
    items = eval(pyb.eval("{_[0].decode():_[1].decode() for _ in configData.db.items()}"))
    items = dict(sorted(items.items(), key=operator.itemgetter(0)))  # 按照key值升序
    # 输出设置项
    print("=" * 100)

    print(f"{format_text('设置项名称')}\t{format_text('设置项设定值')}\t{format_text('设置项说明')}")
    for k, v in items.items():
        print(f"\033[33m{format_text(k)}\t\033[32m{format_text(v)}"
              f"\t\033[38;2;135;206;235m{instructions.get(k, '-')}\033[0m")
    print("=" * 100)


def setting():
    global serial_port, config_path
    pyb = pyboard.Pyboard(serial_port)
    pyb.enter_raw_repl()
    pyb.exec_(pre_cmd)

    command_show(pyb)
    print("* \033[38;2;135;206;235m您拥有修改配置文件的最高权限，请不要轻易修改！\033[0m")
    command_help()

    while True:
        command = input("> ")
        if command.strip() == "":
            continue

        command = command.split()
        try:
            if command[0] == "bye":
                pyb.enter_raw_repl(soft_reset=True)
                pyb.exec_raw_no_follow("__import__('machine').reset()")
                input("已发送重启指令。按下回车退出程序。")
                break
            elif command[0] == "help":
                command_help()
            elif command[0] == "set":
                if len(command) < 2:
                    raise RuntimeError("命令输入错误。需要两个参数。")
                _ = command[1].split('=')
                key, value = _[0], _[1] + ((' ' +  ''.join(command[2:])) if len(command) > 2 else '')
                key = key.replace("'", "\\'")
                value = value.replace("'", "\\'")
                pyb.exec_(
                    f"configData.db[('{key}').encode()] = str('{value}').encode();configData.db.flush()")
                print(f"已设置 \033[33m{key}\033[0m = \033[32m{value}\033[0m 。")
            elif command[0] == "del":
                if len(command) != 2:
                    raise RuntimeError("命令输入错误。需要两个参数。")
                pyb.exec_(
                    f"del configData.db[('{command[1]}').encode()]")
                print(f"已删除 \033[33m{command[1]}\033[0m 。")
            elif command[0] == "show":
                command_show(pyb)
            elif command[0] == "export":
                pyb.fs_get(config_path, "backup.db",
                           progress_callback=lambda x, y: pyboard_utils.fs_put_batch_callback("数据库文件 ", x, y))
                print(f"数据库文件已保存到电脑的 \033[33m{os.path.abspath('backup.db')}\033[0m 。")
            elif command[0] == "import":
                pyb.exec_(f"configData.close()")  # 关掉
                pyb.fs_put(os.path.abspath('backup.db'), config_path,
                           progress_callback=lambda x, y: pyboard_utils.fs_put_batch_callback("数据库文件 ", x, y))
                print(f"数据库文件已恢复到掌控板的 \033[33m{config_path}\033[0m 。")
                pyb.exec_(f"configData=Config()")  # 打开

        except BaseException as e:
            traceback.print_exc()
            print("* 出现错误，" + str(e))

    pyb.close()


def main():
    global config_path, serial_port
    # 输出提示信息
    print("=" * 50)
    print("* TaoLiSystem 系统设置程序 24.7.8 *")
    print("用于调整 TaoLiSystem 系统设置")
    print("\033[33m系统配置文件位置\033[0m：" + "\033[32m" + config_path + "\033[0m")
    if serial_port == "":
        print("\033[33m检测到的掌控板通信串口\033[0m：" + "\033[32m%s\033[0m" % "无")
    else:
        print("\033[33m检测到的掌控板通信串口\033[0m：" + "\033[32m%s\033[0m" % serial_port)
    print("=" * 50)

    # 确认串口
    if serial_port == "" or input(
            "> 目前串口为\033[32m%s\033[0m，请确认对应掌控板串口是否正确？[Y/n]：" % serial_port).lower() == "n":
        serial_port = input("> 请输入掌控板对应的串口：").strip()
        if serial_port == "":
            raise RuntimeError("串口输入有误。")
        print("> 串口设定为 \033[32m%s\033[0m。" % serial_port)

    # 确认配置文件位置
    if input("> 目前配置文件位置为\033[32m%s\033[0m，请确认是否正确？[Y/n]：" % config_path).lower() == "n":
        config_path = input("> 请输入配置文件位置：").strip()
        if config_path == "":
            raise RuntimeError("config_path输入有误。")
        print("> config_path设定为 \033[32m%s\033[0m。" % config_path)

    input("> 按下回车键连接掌控板进行文件配置。")
    setting()


if __name__ == '__main__':
    main()
