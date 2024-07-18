import os
import re
import sys
import ctypes
import shutil
import subprocess
import traceback

make_files = [
    "TaoLiSystem"
]

copy_files = [
    "main.py",
    "boot.py"
]


if len(sys.argv) == 2 and sys.argv[1]:
    print(os.path.abspath(sys.argv[1]))
    root = os.path.abspath(sys.argv[1]).replace("\\", "/")
else:
    root = __file__.replace("\\", "/")

# 文件所在目录
build_file_path = root[:root.rfind("/")]
os.environ['PATH'] = build_file_path + os.pathsep + os.environ.get('PATH', '')
# 导入文件当前目录包，这样做是为了防止程序不在 resource 下运行时出现问题
__import__("requirements_check")  # 检测依赖
pyboard = __import__("pyboard")
pyboard_utils = __import__("pyboard_utils")
serial_ports = __import__('serial.tools.list_ports').tools.list_ports.comports()
if len(serial_ports) != 0:
    serial_port = serial_ports[0].device
else:
    serial_port = ""

# 系统预编译根目录
root = build_file_path[:build_file_path.rfind("/")]

# 获取当前目录
current_directory = os.getcwd()

# 编译保存目录名称
build_name = "_build"

# mpy-cross 对应名称
mpy_cross_name = ""

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


def communicate_broad_execute(ser, msg):
    """与掌控板通信"""
    pyb = pyboard.Pyboard(ser)
    pyb.enter_raw_repl()
    result = pyb.exec_(msg)
    pyb.exit_raw_repl()
    pyb.close()
    return result


def compile_main():
    for file in make_files:
        compile('/', file)

    # 复制文件
    for file in copy_files:
        print("复制文件：" + root + "/" + file)
        shutil.copy(root + "/" + file, current_directory + "/%s/" % build_name + file)


def compile(dir, file):
    """编译文件"""
    global root, current_directory, build_file_path, mpy_cross_name
    if os.path.isdir(root + dir + file):
        try:
            os.mkdir(current_directory + "/%s/" % build_name + dir + file)
        except BaseException as e:
            pass
        for f in os.listdir(root + dir + file):
            compile(dir + file + "/", f)
    else:
        file_name, file_extension = os.path.splitext(file)
        if file_extension == ".py":
            print("正在编译：" + dir + file)
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE  # 设置窗口隐藏
            subprocess.run([build_file_path + "/" + mpy_cross_name,
                            root + dir + file,
                            "-o", current_directory + "/%s/" % build_name + dir + file_name + ".mpy",
                            "-O3"], startupinfo=startupinfo)
        else:
            print("复制文件：" + dir + file)
            shutil.copy(root + dir + file, current_directory + "/%s/" % build_name + dir + file)


def get_mpy_version(version):
    """获取 mpy-cross 对应版本"""
    version_map = {
        (1, 22): "6.2",
        (1, 20): "6.1",
        (1, 19): "6",
        (1, 12): "5",
        (1, 11): "4",
        (1, 9): "3",
        (1, 5): "0",
    }

    major, minor, *_ = map(int, version.split('.'))

    for (v_major, v_minor), mpy_version in sorted(version_map.items(), reverse=True):
        if (major, minor) >= (v_major, v_minor):
            return mpy_version

    return "Unknown version"


def choice_mpy_cross():
    global mpy_cross_name
    print("=" * 50)
    print("* 当前已经存在的 mpy-cross ：")
    files = []
    for file in os.listdir(__file__[:__file__.replace("\\", "/").rfind('/')]):
        if "mpy-cross" in file and os.path.isfile(file):
            files.append(file)

    for i, file in enumerate(files):
        print(f"[{i + 1}] {file}")
    print("=" * 50)
    mpy_cross_name = input("> 请手动输入 mpy-cross 编号或者文件名（路径）（为空自动退出）：").strip()
    if mpy_cross_name.isdigit():
        if 0 <= int(mpy_cross_name) - 1 <= len(files) - 1:
            mpy_cross_name = files[int(mpy_cross_name) - 1]
        else:
            raise RuntimeError("输入的编号不存在。")
    if mpy_cross_name == "":
        raise RuntimeError("没有选择对应版本的 mpy-cross 请自行编译或下载。")


def download_files(ser, filelist):
    pyb = pyboard.Pyboard(ser)
    pyb.enter_raw_repl()

    delete_py = True
    if input("> 是否自动删除掌控板上同名但是未编译的文件？[Y/n]：").lower() == "n":
        delete_py = False

    if pyb.fs_exists("/TaoLiSystem/data/config.ini"):
        pyboard_utils.fs_put_batch(pyb, filelist, "", ignore_files=["/TaoLiSystem/data/config.ini"],
                                   delete_py=delete_py)
    else:
        pyboard_utils.fs_put_batch(pyb, filelist, "", delete_py=delete_py)
    if input("> 传输完成，是否重启掌控板？[Y/n]：").lower() != "n":
        pyb.enter_raw_repl(soft_reset=True)
        pyb.exec_raw_no_follow("__import__('machine').reset()")
        print("已发送重启指令。程序正在退出。")
    pyb.close()


def main():
    global serial_port, build_name, current_directory, root, make_files, mpy_cross_name

    # 输出提示信息
    print("=" * 50)
    print("* Micropython-mpython-掌控板 代码编译程序与下载程序 24.7.8 *")
    print("将 Micropython 的 py 代码转化为 mpy 编译的机器码，\n提高速度，节约内存，有效保护源代码，减少反编译。")
    print("\033[33m白名单中预编译文件/文件夹\033[0m：" + "\033[32m" + str(make_files) + "\033[0m")
    print("\033[33m编译程序目录\033[0m：" + "\033[32m" + build_file_path + "\033[0m")
    print("\033[33m被编译目录\033[0m：" + "\033[32m" + root + "\033[0m")
    print("\033[33m编译后保存目录\033[0m：" + "\033[32m" + current_directory + "/" + build_name + "\033[0m")
    if serial_port == "":
        print("\033[33m检测到的掌控板通信串口\033[0m：" + "\033[32m%s\033[0m" % "无")
    else:
        print("\033[33m检测到的掌控板通信串口\033[0m：" + "\033[32m%s\033[0m" % serial_port)
    print("=" * 50)

    if serial_port == "" or input(
            "> 目前串口为\033[32m%s\033[0m，请确认对应掌控板串口是否正确？[Y/n]：" % serial_port).lower() == "n":
        serial_port = input("> 请输入掌控板对应的串口：").strip()
        if serial_port == "":
            raise RuntimeError("串口输入有误。")
        print("> 串口设定为 \033[32m%s\033[0m。" % serial_port)

    if input("> 是否自动检测对应串口支持的 mpy-cross ？[Y/n]:").lower() == "n":
        choice_mpy_cross()
        print("> 编译程序设定为 \033[32m%s\033[0m。" % mpy_cross_name)
    else:
        print("\033[38;2;135;206;235m* 与掌控板通讯中......\033[0m")
        print("=" * 50)
        try:
            message = communicate_broad_execute(serial_port, "print(list(__import__('os').uname()))")
            if message:
                uname = eval(message)

                print("\033[33m系统平台\033[0m：\033[32m%s\033[0m  "
                      "\033[33m系统发布版本\033[0m：\033[32m%s\033[0m\n"
                      "\033[33m系统版本\033[0m：\033[32m%s\033[0m\n"
                      "\033[33m系统名称\033[0m：\033[32m%s\033[0m" % (uname[0], uname[2], uname[3], uname[4]))

                mpy_cross_name = "mpy-cross-v" + get_mpy_version(uname[2]) + ".exe"
                if os.path.exists(build_file_path + "/" + mpy_cross_name):
                    print(
                        "\033[33m对应的 mpy-cross 版本\033[0m：\033[32mv" + get_mpy_version(uname[2]) + " (存在)\033[0m")
                else:
                    print("\033[33m对应的 mpy-cross 版本\033[0m：\033[32mv" +
                          get_mpy_version(uname[2]) + " \033[31m(不存在)\033[0m")
                    choice_mpy_cross()
            else:
                raise RuntimeError("无法正常获取掌控板串口数据，请重试。")

        except BaseException as e:
            traceback.print_exc()
            print("* 无法正常获取掌控板串口数据，请查看是否串口被占用，请手动选择编译程序。")
            choice_mpy_cross()

        print("=" * 50)
        print("> 编译程序设定为 \033[32m%s\033[0m。" % mpy_cross_name)

    input("> 设置成功，按下回车开始编译。")

    # 编译文件
    if not os.path.exists(current_directory + "/" + build_name):
        os.mkdir(current_directory + "/" + build_name)
        compile_main()
        print("编译完成。")
    else:
        if input("已存在构建过的文件，是否删除并重新构建？[Y/n]").lower() != "n":
            shutil.rmtree(current_directory + "/" + build_name)
            os.mkdir(current_directory + "/" + build_name)
            compile_main()
            print("编译完成。")
        else:
            print("跳过编译。")

    print("=" * 50)
    print("下列文件/文件夹将会在确认后下载到掌控板中：")
    for file in copy_files + make_files:
        print("* " + file)
    print("=" * 50)

    if input("> 是否自动下载到掌控板？此操作不会覆盖原有的配置文件。"
             "\033[38;2;135;206;235m下载过程中请不要随意终止程序。\033[0m[Y/n]：").lower() != "n":
        try:
            download_files(serial_port, [current_directory + "/" + build_name])
        except BaseException as e:
            traceback.print_exc()
            print("出现错误！请手动使用 Thonny 等软件下载到掌控板或者稍后再试！")


if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        traceback.print_exc()
        input("* 按下回车结束程序。")
