# page/home.py 不用想，这就是掌控板主页面的源文件代码。
# 这里将会这设置主页面的样式，所以如果想要换样式的话可以直接更改这里。
# 此页面由 皮卡丘 赞助制作！
# 导入 mpython 支持库
from mpython import *
import time
import _thread
import parrot
import TaoLiSystem.config as config
import TaoLiSystem.wifi

# 引入图片文件
import TaoLiSystem.image

# 字体
import TaoLiSystem.font.arlrdbd as arlrdbdFont
import TaoLiSystem.font.HYShiGuangTiJ as HYShiGuangTiJFont

class HomePage():
    def __init__(self):
        print("看到这一段话说明主页面已经成功被初始化！")
        self.have_wifi_image = TaoLiSystem.image.have_wifi()
        self.no_wifi_image = TaoLiSystem.image.no_wifi()
        self.banner_x = 0
        self.banner_text = "System was made for Pikachu & Niko & TaoLi"
        self.tools = False
        return
    
    def show(self):
        while config.get_value("page") == 'home':
            # 小工具调用
            if touchPad_P.read() <= 400:
                self.tools = True
                self.detailZKB()
            elif touchPad_Y.read() <= 400:
                self.tools = True
                self.detailTZB()
            self.checkEvent()
            # 日期时间的绘制
            oled.fill(0)
            t = time.localtime()
            oled.DispChar_font(arlrdbdFont, "%02d:%02d:%02d" % (t[3], t[4], t[5]), 20, 16)
            oled.DispChar("%04d-%02d-%02d" % (t[0], t[1], t[2]), 34, 34)
            
            # 提示语的绘制
            oled.DispChar("< A 选项             插件 B >", 0, 0)
            oled.bitmap(0, 46, self.no_wifi_image if not TaoLiSystem.wifi.is_connected() else self.have_wifi_image, 16, 16, 1)
            
            # 控制banner的移动
            banner_len = len(self.banner_text)
            banner_text = self.banner_text[ self.banner_x : banner_len ] + " " + self.banner_text[ 0 : self.banner_x ]
            oled.DispChar_font(HYShiGuangTiJFont, banner_text[0:10], 21, 48)
            self.banner_x += 1
            if self.banner_x > len(self.banner_text):
                self.banner_x = 0
            
            
            
            oled.show()
    
    def detailZKB(self):
        """掌控板信息"""
        while self.tools:
            oled.fill(0)
            oled.DispChar("掌控板传感器信息", 0, 0)
            oled.hline(0, 14, 128, 1)
            oled.DispChar("光线传感器亮度:%d"  % (light.read()) ,0 ,16)
            oled.DispChar("声音值:%d" % (sound.read()) ,0 ,32)
            oled.DispChar("加速度(x,y,z):(%d,%d,%d)" % (accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()), 0, 48)
            oled.show()
    def detailTZB(self):
        """拓展版信息"""
        while self.tools:
            oled.fill(0)
            oled.DispChar("拓展板信息", 0, 0)
            oled.hline(0, 14, 128, 1)
            try:
                oled.DispChar("电池电量:%dmV"  % (parrot.get_battery_level()) ,0 ,16)
            except:
                oled.DispChar("电池电量-mV(未连接拓展板)" ,0 ,16 , 1, True)
            oled.show()
    
    def checkEvent(self):
        """初次之外要看看用户是否按下的按钮"""

        if button_a.value() + button_b.value() == 0:
            pass
        elif button_a.value() == 0:
            print("按下 A 键，进入 选项")
            config.set_value("page", "setting") 
            return True
        elif button_b.value() == 0 and not self.tools:
            print("按下 B 键，进入 插件")
            config.set_value("page", "plugin") 
            return True
        elif button_b.value() == 0 and self.tools:
            self.tools = False
            time.sleep(0.5)