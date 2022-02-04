# 用于选择页面的模块
from mpython import *
import _thread

class ItemSelector():
    def __init__(self, items, title):
        self.items = items
        self.title = title
        self.items_len = len(self.items)
        self.a = -1 if self.items_len == 0 else 0  # 当前选择项
        self.final_item = ""  # 最终决定的项目
        self.final_item_a = None  # 最终决定项目的id
        return

                    
    
    def start(self):
        # 绘制
        oled.fill(0)
        oled.DispChar(self.title, 0, -2)
        oled.hline(0, 14, 128, 1)
        while True:
            if self.final_item_a != None:
                final_item = self.final_item
                del self
                return final_item
            
            oled.DispChar("%d/%d" % (self.a + 1, self.items_len), 100, -2)
            oled.fill_rect(0, 15, 128, 48, 0)
            
            if self.items_len == 0:
                oled.DispChar("这里什么也没有哦", 15, 32, 1, True)
            else:
                for i in range(self.a, min(self.a + 3, self.items_len)):
                    oled.DispChar(self.items[i] + (" <" if self.a == i else ""), 0, 16 + 16 * (i - self.a), 1, True)
                
            oled.show()
            
            while True:
                if touchPad_T.read() <= 400:
                    self.a = 0
                    break
                elif touchPad_H.read() <= 400:
                    self.a = self.items_len - 1
                    break
                elif touchPad_P.read() <= 400:
                    self.a = max(self.a - 1, -1 if self.items_len == 0 else 0)
                    break
                elif touchPad_N.read() <= 400:
                    self.a = min(self.a + 1, self.items_len - 1)
                    break
                if button_b.value() == 0:
                    print("按下 B 键，取消选择")
                    self.final_item = ""
                    self.final_item_a = -1
                    break
                elif button_a.value() == 0:
                    if self.items_len == 0:
                        print("按下 A 键，无选择项，取消选择")
                        self.final_item = ""
                        self.final_item_a = -1
                        break
                    else:
                        print("按下 A 键，选择", self.items[self.a])
                        self.final_item = self.items[self.a]
                        self.final_item_a = self.a
                        break
            
            
            
            

            
