# morseType.py 用摩尔斯电码打字。
# 此页面由以赏想出来，由皮卡丘支持制作！
from mpython import *
import time

# 显示区
#
#
#
#-----------------------
# 打字区
#

morseDict = {
    'A': '.-',     'B': '-...',   'C': '-.-.',
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',

    '0': '-----',  '1': '.----',  '2': '..---',
    '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.',
    
    ' ': '-....-', '.': '.-.-.-', ':': '---...', '-': '-..--', ';': '-.-.-.',
    '?': '..--..', '=': '-...-', '\'': '.----.', '/': '-..-.',
    '!': '-.-.--', '-':'-....-', '_': '..--.-', '"': '.-..-.',
    '(': '-.--.', ')': '-.--.-', '$' :'...-..-','&': '....',
    '@': '.--.-.'
}

morseDict = dict(zip(morseDict.values(), morseDict.keys()))

def morse2utf8(text):
    try:
        text = text.replace(".", "0").replace("-", "1")
        return chr(int(text, 2))
    except:
        return ""

class MorseType():
    def __init__(self):
        """启动程序"""
        # 转义之后的文本存放
        self.text = ""
        # 光标位置
        self.pos = -1
        # 临时电码
        self.temp = ""
        # 大小写指示
        self.capital = True
        print("摩尔斯键盘已初始化！")
        return
    
    def start(self):
        """开始打字"""
        while True:
            oled.fill(0)
            oled.hline(0, 48, 128, 1)

            oled.DispChar(self.text[:self.pos + 1] + "▎" + self.text[self.pos + 1:], 0, 0, 1, True)

                
            
            
            oled.DispChar("大" if self.capital else "小", 115, 50, 1, False)  
            oled.DispChar(self.temp, 0, 50, 1, False)
            oled.show()
            
            # 记录当前时间
            t = time.ticks_ms()
            while True:
                time.sleep_ms(50)
                if button_a.value() + button_b.value() == 0:
                    _ = self.text
                    del self
                    return _
                elif button_a.value() == 0:
                    self.temp += "."
                    t = time.ticks_ms()  # 按了就重置时间
                    break
                elif button_b.value() == 0:
                    self.temp += "-"
                    t = time.ticks_ms()  # 按了就重置时间
                    break
                if time.ticks_ms() - t >= 600:  # 600ms 没按就转义
                    _ = morseDict.get(self.temp, morse2utf8(self.temp))
                    if not self.capital:
                        _ = _.lower()
                    if len(self.text) == 0:
                        self.text += _
                    else:
                        self.text = self.text[:self.pos + 1] + _ + self.text[self.pos + 1:]
                    self.pos += len(_)
                    self.temp = ""
                    break
                
                if touchPad_P.read() <= 400:
                    self.pos = max(self.pos - 1, -1)
                    break
                elif touchPad_N.read() <= 400:
                    self.pos = min(self.pos + 1, len(self.text) - 1)
                    break
                elif touchPad_Y.read() <= 400:
                    self.capital = not self.capital
                    break
                elif touchPad_O.read() <= 400:
                    self.text = self.text[:self.pos] + _ + self.text[self.pos + 1:]
                    self.pos = max(self.pos - 1, 0)
                    break

