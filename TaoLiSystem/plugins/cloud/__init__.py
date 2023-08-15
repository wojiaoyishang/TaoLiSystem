from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *

from .function import *

if not utils.isEnableWIFI():
    sysgui.messageBox("请先连接 WIFI。", yes_text="好的")
    raise ValueError("用户终止执行。")

selected_id = 0

while True:
    selected_id = sysgui.itemSelector("选择功能", ["随机皮卡丘照片", "随机恐怖故事", "随机笑话", "TFT 屏幕引脚设置"], selected_id)
    
    if selected_id is None:
        break
    
    if selected_id == 0:  # 随机皮卡丘照片
        randpikachu()
    if selected_id == 1:  # 随机恐怖故事
        randHorrorStory()
    elif selected_id == 3:
        tft_pin_setting()