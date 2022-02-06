# boot.py 被定义为启动文件，可能是掌控板在一开始运行时就会最先调用这个文件吧
# 嘿！欢迎使用陶丽系统，此系统由我叫以赏开发，献给高一信息老师陶丽，同时也献给皮卡丘和 OneShot 中的 Niko ！
# 你正在阅读这段文字，意味着你正在阅读我留下的彩蛋，同时也是在阅读我的思想。
# 在之后的注释中，也会出现这样的文字。不妨你可以找一找？
# 这里是陶丽系统最开始的启动页面，讲真，我还拿不准到底该如何去写......

# 导入 mpython 支持库
from mpython import *
import time  # 时间
import _thread   # 导入线程模块
# 引入图片文件
import TaoLiSystem.image
import micropython
micropython.alloc_emergency_exception_buf(10000)

Loading = True # 控制是否继续加载

def Loading_page():
    boot_image = TaoLiSystem.image.boot_image()
    i = 1  # 控制加载点的个数
    while Loading:
        time.sleep(0.5)
        if not Loading:
            break
        oled.fill(0)
        oled.bitmap(0, 8, boot_image, 48, 48, 1)
        oled.DispChar("正在启动系统", 54, 23)
        oled.DispChar("·" * i, 70, 36)
        if not Loading:
            break
        oled.show()
        i = 1 if i >= 6 else i + 1
        
    del boot_image
    _thread.exit()

_thread.start_new_thread( Loading_page, () )   # 启动加载线程