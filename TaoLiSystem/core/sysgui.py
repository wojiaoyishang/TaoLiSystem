# 实用的代码汇集与系统的一些内置功能
import time
import ustruct

from mpython import *

from ..modules import bin2picture
from TaoLiSystem.core.config import *

# 便于绘制数字
def draw_string_from_bin(x, y, fp, string, r=None):
    r = r if r else bin2picture.get_bin_data_pos(fp, list(string))
    i = 0
    for s in string:
        w, _ = bin2picture.print_from_bin_by_pos(x + i, y, fp, r.get(s, 0))
        i += w
    return w

# 居中绘制
def draw_string_center(text, y, mode=TextMode.normal, ex=False):
    # 支持多行内容
    i = 0
    text = text.split("\n")
    for t in text:
        # 获取字体长度
        text_width = get_character_width(t)
        if not ex:
            oled.DispChar(t, int(128 / 2 - text_width / 2) + i * 16, y, mode)
        else:
            oled.DispChar(t, int(128 / 2 - text_width / 2), int(64 / 2 - 16 * len(text) / 2) - y + i * 16, mode)
        i += 1

# 画空框
def draw_rect_empty(x1, y1, x2, y2, function=None, no_fill=False):
    if not no_fill:
        oled.fill_rect(x1 + 1, y1 + 1, x2 - 2, y2 - 2, 0)
    if function:
        function()
    oled.rect(x1, y1, x2, y2, 1)   

def get_character_width(s):
    """
    获取输入字符串中每个字符的宽度。
    
    参数:
    s (str): 需要获取字符宽度的字符串。

    返回:
    int: 字符串的宽度。
    """
    width = 0
    for character in s:
        if character == "" or character is None:
            return 0
        character_data = oled.f.GetCharacterData(character)
        if character_data is None:
            return None
        width += ustruct.unpack('HH', character_data[:4])[0] + 1  # 加一为间距

    return width - 1  # 减掉最后的间距

def selectionBox(items, selected_id=0):
    """
    在给定列表的内容上显示一个选择框。

    参数:
    items (list): 用于显示在选择框中的项目列表。
    selected_id (int, optional): 默认选择的项目ID，默认为0。

    返回:
    int/None: 用户选择的项目ID，如果用户取消选择，则返回None。
    """
    draw_rect_empty(1, 1, 126, 62)
    
    a_pressed = b_pressed = False
    
    # 记录原本按钮绑定函数
    button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed

    def button_a_callback(_):
        nonlocal a_pressed
        a_pressed = True

            
    def button_b_callback(_):
        nonlocal b_pressed
        b_pressed = True
            
    button_a.event_pressed = button_a_callback
    button_b.event_pressed = button_b_callback
    
    
    while True:
        
        draw_rect_empty(2, 2, 126, 62)
        draw_string_center("<A> <P  %d/%d  N> <B>" % (selected_id + 1, len(items)), 50, mode=TextMode.trans)
        draw_string_center(items[selected_id], 5, ex=True)
        
        oled.show()
        
        while True:
            if a_pressed:
                button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
                return selected_id
            elif b_pressed:
                button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
                return None
            
            if touchPad_T.read() <= touchPad_sensitivity:
                selected_id = 0
                break
            elif touchPad_H.read() <= touchPad_sensitivity:
                selected_id = len(items) - 1
                break
            elif touchPad_P.read() <= touchPad_sensitivity:
                selected_id = max(selected_id - 1, 0)
                break
            elif touchPad_N.read() <= touchPad_sensitivity:
                selected_id = min(selected_id + 1, len(items) - 1)
                break

def itemSelector(title, items, selected_id=0):
    """
    显示一个物品选择器。

    参数:
    title (str): 选择器的标题。
    items (list): 可供选择的物品列表。
    selected_id (int, optional): 默认选择的物品ID，默认为0。

    返回:
    int/None: 用户选择的物品ID，如果用户取消选择，则返回None。
    """
    if selected_id > len(items) - 1:
        selected_id = len(items) - 1
    a_pressed = b_pressed = False
    
    # 记录原本按钮绑定函数
    button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed
    

    def button_a_callback(_):
        nonlocal a_pressed
        a_pressed = True

            
    def button_b_callback(_):
        nonlocal b_pressed
        b_pressed = True
            
    button_a.event_pressed = button_a_callback
    button_b.event_pressed = button_b_callback
        
    while True:
        oled.fill(0)
        oled.DispChar(title, 0, -2)
        oled.hline(0, 14, 128, 1)

        # 根据selected_id确定显示哪三个项目
        start_id = max(0, min(len(items) - 3, selected_id - 1))
        display_items = items[start_id:start_id + 3]

        # 为每个项目显示文本
        for i, item in enumerate(display_items):
            oled.DispChar(item, 0, 16 * (i + 1))

        # 为选中的项目填充矩形
        if len(display_items) > 0:
            oled.fill_rect(0, 16 + 16 * (selected_id - start_id), 128, 16, 1)
            oled.DispChar(display_items[selected_id - start_id], 0, 16 + 16 * (selected_id - start_id), mode=TextMode.rev)

        
        oled.show()
        
        while True:
            if a_pressed:
                button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
                return selected_id
            elif b_pressed:
                button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
                return None
            
            if touchPad_T.read() <= touchPad_sensitivity:
                draw_rect_empty(1, 1, 126, 62)
                selected_id = 0
                break
            elif touchPad_H.read() <= touchPad_sensitivity:
                selected_id = len(items) - 1
                break
            elif touchPad_P.read() <= touchPad_sensitivity:
                selected_id = max(selected_id - 1, 0)
                break
            elif touchPad_N.read() <= touchPad_sensitivity:
                selected_id = min(selected_id + 1, len(items) - 1)
                break

def messageBox(content, yes_text="好的", no_text=None, button_line=False, content_fun=None):
    """
    显示一个消息框。

    参数:
    content (str): 消息框中的文本。为 None 不绘制任何文本内容，请传入 content_fun 来绘制。
    yes_text (str, optional): 确认按钮的文本，默认为"好的"。
    no_text (str, optional): 取消按钮的文本，默认为None。
    button_line (bool, optional): 是否在按钮之间换行，默认为False。
    content_fun (function, optional): 尽在 content 为 None 时调用。

    返回:
    bool: 用户按下确认按钮返回True，否则返回False。
    """
    
    
    if content is None:
        draw_rect_empty(1, 1, 126, 62, content_fun)
    else:
        draw_rect_empty(1, 1, 126, 62, lambda : draw_string_center(content + "\n<A " + yes_text + ">" +
                                    (((" " if not button_line else "\n") +
                                      "<B " + no_text + ">") if no_text is not None else ""), 0, ex=True))
        
        
    a_pressed = b_pressed = False
    
    # 记录原本按钮绑定函数
    button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed

    def button_a_callback(_):
        nonlocal a_pressed
        a_pressed = True

            
    def button_b_callback(_):
        nonlocal b_pressed
        b_pressed = True
            
    button_a.event_pressed = button_a_callback
    button_b.event_pressed = button_b_callback
    
    oled.show()
    while True:
        
        if a_pressed:
            button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
            return True
        elif b_pressed:
            button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
            return False

def tipBox(content, t=3):
    """
    显示一个提示框。

    参数:
    content (str): 提示框中的文本。
    t (int, optional): 提示框显示的时间（秒），默认为3秒。
    """
    button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed
    # 提示
    draw_rect_empty(1, 1, 126, 62, lambda : draw_string_center(content, 0, ex=True))
    oled.show()
    time.sleep(t)
    button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o

def txtStreamReader(stringIO, title, bookmarks=[], screen_width=128+8):
    """
    实现文本流阅读。

    参数:
    stringIO (io.StringIO): 需要读取的文本流。
    title (str): 阅读器的标题。
    bookmarks (list, optional): 书签，默认为空列表，列表内为列表如["书签1", 0]，第一个为书签名称，第二个为书签位置

    返回:
    bool/None: 用户选择退出阅读时返回True，如果用户取消退出操作，则继续阅读并返回None。
    """
    a_pressed = b_pressed = False
    
    # 记录原本按钮绑定函数
    original_a_callback, original_b_callback = button_a.event_pressed, button_b.event_pressed

    def button_a_callback(_):
        nonlocal a_pressed
        a_pressed = True

    def button_b_callback(_):
        nonlocal b_pressed
        b_pressed = True
            
    button_a.event_pressed = button_a_callback
    button_b.event_pressed = button_b_callback
    
    history_seek = []  # 历史光标位置
    oled.hline(0, 28, 128, 1)
    bookmarks_pos = None  # 是否移动书签

    while True:
        begin_seek = stringIO.tell()  # 开始光标位置
        oled.fill(0)
        text = ""
        text_width = 0
        t = True
        for line_number in range(64 // 16):
            while t:
                t = stringIO.read(1)
                text += t
                if t == "\n":  # 换行
                    single_text_width = 0
                    break
                single_text_width = get_character_width(t)
                text_width += single_text_width
                if text_width > screen_width - single_text_width:
                    break
            if t:
                _ = text[-1]  # 记录多的字符
                text_width = single_text_width
                text = text[:-1]
                if bookmarks_pos is None:
                    oled.DispChar(text, 0, line_number * 16)
                    oled.show()
                if _ != "\n":
                    text = _
                else:
                    text = ""
            else:
                if bookmarks_pos is None:
                    oled.DispChar(text, 0, line_number * 16)
                    oled.show()
                break
        
        if bookmarks_pos is not None and stringIO.tell() < bookmarks_pos:
            history_seek.append(begin_seek)
            continue
        elif bookmarks_pos is not None:
            bookmarks_pos = None
            oled.show()
            continue
        
        
        while True:
            if a_pressed:
                a_pressed = False
                select_id = itemSelector("功能", ["结束阅读", "详情"])
                if select_id is None:
                    stringIO.seek(begin_seek)
                    break
                
                if select_id == 1:
                    messageBox("阅读内容：\n" + title, yes_text="好的")
                elif select_id == 0:
                    button_a.event_pressed, button_b.event_pressed = original_a_callback, original_b_callback
                    return
                    
                stringIO.seek(begin_seek)
                break
            elif b_pressed:
                b_pressed = False
                if messageBox("确认退出阅读？", yes_text="是的", no_text="取消/帮助", button_line=True):
                    button_a.event_pressed, button_b.event_pressed = original_a_callback, original_b_callback
                    return
                else:
                    if messageBox("你想要？", yes_text="取消", no_text="帮助"):
                        stringIO.seek(begin_seek)
                        break
                    else:
                        messageBox("A功能菜单\nB退出/帮助", yes_text="下一步")
                        messageBox("P上一页 N下一页\nT进度 H书签", yes_text="下一步")
                        stringIO.seek(begin_seek)
                        break
            
            if touchPad_P.read() <= touchPad_sensitivity and len(history_seek):
                stringIO.seek(history_seek.pop())
                break
            elif touchPad_T.read() <= touchPad_sensitivity:
                # 获取阅读百分比
                now_seek = stringIO.tell()
                stringIO.seek(0, 2)
                per = round(now_seek / stringIO.tell() * 100, 2)
                stringIO.seek(begin_seek)  # 回到一开始的位置
                messageBox("阅读百分比：" + str(per) +"%")
                break
            elif touchPad_H.read() <= touchPad_sensitivity:
                # 书签
                select_id = itemSelector("书签", ["跳转", "添加书签"])
                
                if select_id == None:
                    stringIO.seek(begin_seek)
                    break
                
                if select_id == 0:
                    if len(bookmarks) == 0:
                        tipBox("没有任何书签哦！")
                    else:
                        bookmark_id = itemSelector("选择书签", [b[0] for b in bookmarks])
                        bookmarks_pos = bookmarks[bookmark_id][1]
                        tipBox("正在移动阅读位置......")
                        while history_seek and history_seek[-1] >= bookmarks_pos:
                            history_seek.pop()
                        if history_seek:
                            stringIO.seek(history_seek[-1])
                        else:
                            stringIO.seek(0)
                        break
                else:
                    bookmarks.append(["书签" + str(len(bookmarks) + 1), begin_seek])
                    tipBox("书签" + str(len(bookmarks)) + "已添加！", 1)
                stringIO.seek(begin_seek)
                break
            elif touchPad_N.read() <= touchPad_sensitivity:  # 下一页
                if t == "":
                    if messageBox("阅读已结束是否退出？", yes_text="是的", no_text="取消"):
                        button_a.event_pressed, button_b.event_pressed = original_a_callback, original_b_callback
                        return
                    else:
                        stringIO.seek(begin_seek)
                else:
                    history_seek.append(begin_seek)
                break

def textTypeBox(text="", all_text = ["0123456789", "abcdef", "ghijkl", "mnopqr", "stuvwx", "yz", ".?!=;:*"], input_callback=None):
    """
    输入文本
    """
    if input_callback is None:
        input_callback = lambda origin_text, input_text, text_pos: (origin_text[:text_pos] + input_text + text[text_pos:], text_pos + 1)
        
    a_pressed = b_pressed = False
    
    # 记录原本按钮绑定函数
    original_a_callback, original_b_callback = button_a.event_pressed, button_b.event_pressed

    def button_a_callback(_):
        nonlocal a_pressed
        a_pressed = True

    def button_b_callback(_):
        nonlocal b_pressed
        b_pressed = True
            
    button_a.event_pressed = button_a_callback
    button_b.event_pressed = button_b_callback
    
    now_pos = 0
    choice_pos = 0
    choice_text = None
    show_tip = [True, True, True]
    capsLock = False
    function_mode = False
    
    text_pos = len(text)
    
    while True:
        oled.fill(0)
        oled.hline(0, 28, 128, 1)
        
        display_text = ""
        
        oled.DispChar(text[:text_pos] + "▏" + text[text_pos:], 0, 0, auto_return=True)
        if function_mode:  # 功能模式
            if show_tip[0]:
                show_tip[0] = False
                draw_rect_empty(14, 1, 100, 26)
                draw_string_center("按B退出", 18, ex=True)
            draw_string_center("[←P] [N→]\n[T 回删] [H 空格]", -14, ex=True)
        elif choice_text:  # 开始打字
            if show_tip[1]:
                show_tip[1] = False
                draw_rect_empty(14, 1, 100, 26)
                draw_string_center("<P <<T A H>> N>", 18, ex=True)
            oled.DispChar("<Y 返回", 0, 48)
            for i, t in enumerate(choice_text):
                if capsLock:
                    t = t.upper()
                if i == choice_pos:
                    display_text += "[> %s <] " % t
                else:
                    display_text += "%s " % t
            draw_string_center(display_text, -8, ex=True)
            oled.DispChar("O↑" if not capsLock else "O↓", 110, 48)
        else:  # 选择字组
            if show_tip[2]:
                show_tip[2] = False
                draw_rect_empty(14, 1, 100, 26)
                draw_string_center("Y-O选择 B功能", 18, ex=True)
            oled.DispChar("<P", 0, 48)
            for i, c in enumerate(all_text[now_pos:now_pos+4]):
                if i == 1 or i == 3:
                    display_text += " "
                elif i == 2:
                    display_text += "\n"
                display_text += "[%s %s-%s]" % ("YTHO"[i], c[0], c[-1])
            draw_string_center(display_text, -14, ex=True)
            oled.DispChar("N>", 112, 49)
                
        oled.show()
        while True:
            if a_pressed:
                a_pressed = False
                if choice_text is None or function_mode:
                    if messageBox("完成输入？", yes_text="是的", no_text="再想想"):
                        button_a.event_pressed, button_b.event_pressed = original_a_callback, original_b_callback
                        return text
                elif choice_text:
                    text, text_pos = input_callback(text, choice_text[choice_pos].upper() if capsLock else choice_text[choice_pos], text_pos)
                break
            elif b_pressed:
                b_pressed = False
                function_mode = not function_mode
                break
            
            if touchPad_P.read() <= touchPad_sensitivity:  # 向前
                if function_mode:
                    text_pos = max(0, text_pos - 1)
                elif not choice_text:
                    now_pos = max(0, now_pos - 4)
                else:
                    choice_pos = max(0, choice_pos - 1)
                break
            elif touchPad_N.read() <= touchPad_sensitivity:  # 向后
                if function_mode:
                    text_pos = min(text_pos + 1, len(text))
                elif not choice_text:
                    now_pos = min(len(all_text) - 4, now_pos + 4)
                else:
                    choice_pos = min(choice_pos + 1, len(choice_text) - 1)
                break
            elif touchPad_Y.read() <= touchPad_sensitivity:
                if function_mode:
                    pass
                elif not choice_text:
                    choice_text = all_text[now_pos]
                else:
                    choice_text = None
                    choice_pos = 0
                break
            elif touchPad_T.read() <= touchPad_sensitivity:
                if function_mode:
                    if text_pos > 0:
                        text = text[:text_pos - 1] + text[text_pos:]
                        text_pos -= 1
                elif not choice_text:
                    if now_pos + 1 <= len(all_text) - 1:
                        choice_text = all_text[now_pos + 1]
                else:
                    choice_pos = 0
                break
            elif touchPad_H.read() <= touchPad_sensitivity:
                if function_mode:
                    text = text[:text_pos] + " " + text[text_pos:]
                    text_pos += 1
                elif not choice_text:
                    if now_pos + 2 <= len(all_text) - 2:
                        choice_text = all_text[now_pos + 2]
                else:
                    choice_pos = len(choice_text) - 1
                break
            elif touchPad_O.read() <= touchPad_sensitivity:
                if not choice_text:
                    if now_pos + 3 <= len(all_text) - 3:
                        choice_text = all_text[now_pos + 3]
                else:
                    capsLock = not capsLock
                break
               

