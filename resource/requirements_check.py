# 自动检测是否安装依赖 By：Yishang
import sys
import subprocess

print("* 正在进行依赖检查......")

try:
    import serial
except ImportError:
    if input("> 检查到缺少依赖 serial 是否安装？[Y/n]：").strip() != "n":
        subprocess.run(
            [sys.executable.replace("pythonw.exe", "python.exe"),
             "-m", "pip", "install", "pyserial", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/"])
        try:
            import serial
        except ImportError:
            print("* 依赖安装失败，请重试。")
            exit()
    else:
        exit()

print("* 依赖已经全部安装。")
