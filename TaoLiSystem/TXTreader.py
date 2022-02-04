# TXTreader.py 用于一个简单的文本阅读
# 什么？你怎么知道这里会有一个阅读器？

# 导入 mpython 支持库
from mpython import *

# 食用说明：
# A 向上翻页、B 向下翻页、T 显示基本信息、H 退出阅读、P 上移一行、N 下移一行

class TXTreader():
    def __init__(self, content, title):
        """最初的入口点，要提供 文章标题、文章内容"""
        # 经过测试一页可以显示 40 个中文汉字，一行 10 个中文字
        self.title = title
        self.content = content + "\n阅读结束,按 H 退出"
        # 当前光标行数
        self.i = 0
        # 屏幕输出行
        self.lines = self._format(self.content)
        del self.content
        
    def start(self):
        """开始阅读"""
        while True:
            self._show()
            while True:
                if button_a.value() == 0:
                    self.i = max(self.i - 4, 0)
                    break
                elif button_b.value() == 0:
                    self.i = min(self.i + 4, len(self.lines) - 1)
                    break
                if touchPad_T.read() <= 400:
                    oled.fill(0)
                    oled.DispChar("文章标题：" + str(self.title), 0, 0, 1, True)
                    oled.DispChar("阅读百分比：%.2f" % (min(self.i + 4, len(self.lines) - 1) / (len(self.lines) - 1) * 100) + "%", 0, 16, 1, True)
                    oled.DispChar("(再次点击 T 退出)", 0, 48, 1, True)
                    oled.show()
                    while True:
                        if touchPad_T.read() <= 400:
                            self._show()
                            break
                elif touchPad_P.read() <= 400:
                    self.i = max(self.i - 1, 0)
                    break
                elif touchPad_N.read() <= 400:
                    self.i = min(self.i + 1, len(self.lines) - 1)
                    break
                elif touchPad_H.read() <= 400:
                    del self
                    return

    def _show(self):
        """显示文本的过程"""
        oled.fill(0)
        try:
            oled.DispChar(self.lines[self.i], 0, 0)
            oled.DispChar(self.lines[self.i + 1], 0, 16)
            oled.DispChar(self.lines[self.i + 2], 0, 32)
            oled.DispChar(self.lines[self.i + 3], 0, 48)
        except:
            pass
        oled.show()
    
    def _format(self, text):
        """格式化输出文本"""
        lines = []
        line_len = 0
        t = ""
        z = 0
        for s in text:
            if u'\u4e00' <= s <= u'\u9fff':
                line_len += 6.5
            else:
                line_len += 3.5
            t += s
            z += 1
            if line_len >= 60 or s == "\n":
                lines.append(t)
                t = ""
                line_len = 0

        
        # 最后
        lines.append(t)

        if len(lines) < 4:
            lines = lines + [""] * (4 - len(lines))
        
        
        return lines
    
