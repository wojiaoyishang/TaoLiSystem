# main.py 被定义为主要文件，紧跟着 boot.py 之后，系统会自动调用
# 怎么说呢...... 噩梦开始了......
# 特别谢明：此页面由 Niko 测试 BUG，由 皮卡丘 初步试验。

# 导入 mpython 支持库
from mpython import *
import time  # 时间
import gc
import _thread   # 导入线程模块

# 导入陶丽库中的模块
import TaoLiSystem.function
import TaoLiSystem.config as config
from TaoLiSystem.ItemSelector import ItemSelector as ItemSelector

# 陶丽库中的页面模块
from TaoLiSystem.page.home import HomePage as HomePage  # 主页面
from TaoLiSystem.page.setting import SettingPage as SettingPage  # 设置页面
from TaoLiSystem.page.plugin import PluginPage as PluginPage  # 插件

# 系统启动时的变量
config.set_value("page", "home")  # 用于指示当前处于的页面
config.set_value("wifiSSID", "")  # 当前连接的wifi


# 这里开始进行加载配置
import TaoLiSystem.loader

# 给加载插件用的
def loadPlugin(exec_code):
    # 如果有插件加载那么也关闭加载
    global Loading
    Loading = False
    oled.fill(0)
    oled.show()
    gc.collect()
    exec(exec_code, globals(), locals())
    del exec_code
    gc.collect()

gc.isenabled()  # 进行内存碎片自动收集
TaoLiSystem.loader.main(loadPlugin)  # 开始正式加载

# 加载在 boot.py 中被定义了，使用可以直接修改
Loading = False

# 初始化页面
homePage = HomePage()
settingPage = SettingPage()
pluginPage = PluginPage(loadPlugin)


# 先清个屏
oled.fill(0)
oled.show()
time.sleep(1)



while True:
    try:
        homePage.show()
        settingPage.show()
        pluginPage.show()
    except MemoryError as error:
        TaoLiSystem.function.loadingPage("出现了内存错误！请稍后再试！", 10, 2)
        continue
        

