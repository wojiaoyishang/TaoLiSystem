# 系统入口

# =======================调试命令=======================
from mpython import *
if button_a.value() == 0:  # 按下 A 键就退出。防止卡电脑调试。
    raise BaseException("Stop by user.")

# =======================传递参数=======================
from TaoLiSystem.core import utils
def importModule(name):  # 导入模块函数，只有在 main.py 中才能让 exec 不出问题
    _ = []
    exec("import " + name + " as pikachu;_.append(pikachu)", {"_": _})
    return _[0]

utils.importModule = importModule

# =======================系统初始化=======================
from TaoLiSystem.core import loader
loader.before_init()  # 初始化之前执行
loader.init() 
loader.after_init()  # 初始化之后执行
loader.clean()  # 删去初始化的所有内容
loader.main_loop()  # 进入系统主循环
    
    



