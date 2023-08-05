# 天气函数的定义
import sys
import urequests

import weather_icon as seniverse  # 没想到掌控板内置了图标

from mpython import *

from TaoLiSystem.core import sysgui, utils
from TaoLiSystem.core.config import *


# 填入你的知心天气的KEY，这里我使用官方示例中的KEY
URL_DAILY_WEATHER_API = "https://api.seniverse.com/v3/weather/daily.json?key=SMhSshUxuTL0GLVLS"  # 今日天气
URL_NOW_WEATHER_API = "https://api.seniverse.com/v3/weather/now.json?key=SMhSshUxuTL0GLVLS"  # 此刻天气
URL_SUGGESTION_WEATHER_API = "https://api.seniverse.com/v3/life/suggestion.json?key=SMhSshUxuTL0GLVLS"  # 今日建议

def draw_main():
    if "wifi" not in global_var or not global_var.get("wifi").sta.isconnected():
        draw_error()
        return
    if global_var.get('weather_got') is None:
        sysgui.draw_string_center("▲今日天气▲", 0)
        sysgui.draw_string_center("按下 P 键", 16)
        sysgui.draw_string_center("获取今日天气", 32)
        sysgui.draw_string_center("o*￣▽￣*ブ", 48)
    elif global_var['daily_weather'] is None:
        sysgui.draw_string_center("▲获取天气失败▲", 0)
        sysgui.draw_string_center("服务器出错", 16)
        sysgui.draw_string_center("按下 P 再试", 32)
        sysgui.draw_string_center("/ㄒoㄒ/~~", 48)
    else:
        # 处理一下
        today = global_var['daily_weather']['results'][0]['daily'][0]['date'][-5:]         # 当前日期，显示“月-日”
        todayHigh = global_var['daily_weather']['results'][0]['daily'][0]['high']          # 最高温度
        todaylow = global_var['daily_weather']['results'][0]['daily'][0]['low']            # 最低温度
        city = global_var['daily_weather']['results'][0]['location']['name']               # 地理位置
        if time.localtime()[3] >= 12:  # 12点之前参考早上
            code = global_var['daily_weather']['results'][0]['daily'][0]['code_day']
            text = global_var['daily_weather']['results'][0]['daily'][0]['text_day']
        else:
            code = global_var['daily_weather']['results'][0]['daily'][0]['code_night']
            text = global_var['daily_weather']['results'][0]['daily'][0]['text_night']
        oled.fill(0)
        oled.bitmap(16, 12, seniverse.from_code(int(code)), 38, 38, 1)                   # 显示当前天气现象图标
        oled.DispChar(text, 78, 16)
        oled.DispChar("%s~%s℃"  % (todaylow, todayHigh), 68, 32)       # 显示今日最低、最高气温
        sysgui.draw_string_center("今日天气 " + today, 1)
        oled.fill_rect(0, 49, 128, 64, 1)
        if global_var.get('now_weather'):
            nowText = global_var['now_weather']['results'][0]['now']['text']                   # 天气现象文字
            nowTemper = global_var['now_weather']['results'][0]['now']['temperature']          # 温度
            sysgui.draw_string_center("%s 此刻:%s %s℃" % (city, nowText, nowTemper), 49, mode=TextMode.rev)

def draw_pre(i):
    if 'daily_weather' not in global_var:
        return
    today = global_var['daily_weather']['results'][0]['daily'][i]['date'][-5:]         # 当前日期，显示“月-日”
    todayHigh = global_var['daily_weather']['results'][0]['daily'][i]['high']          # 最高温度
    todaylow = global_var['daily_weather']['results'][0]['daily'][i]['low']            # 最低温度
    text_day = global_var['daily_weather']['results'][0]['daily'][i]['text_day']
    text_night = global_var['daily_weather']['results'][0]['daily'][i]['text_night']
    rainfall = global_var['daily_weather']['results'][0]['daily'][i]['rainfall']  # 降水量
    precip = global_var['daily_weather']['results'][0]['daily'][i]['precip']  # 降水概率
    wind_direction = global_var['daily_weather']['results'][0]['daily'][i]['wind_direction']  # 风向文字
    wind_speed = global_var['daily_weather']['results'][0]['daily'][i]['wind_speed'] # 风速
    wind_scale = global_var['daily_weather']['results'][0]['daily'][i]['wind_scale'] # 风级
    humidity = global_var['daily_weather']['results'][0]['daily'][i]['humidity'] # 湿度
    oled.fill(0)
    sysgui.draw_string_center("%s %s~%s℃" % (today, todaylow, todayHigh), 0)
    sysgui.draw_string_center("(早)%s (晚)%s" % (text_day, text_night), 16)
    sysgui.draw_string_center("(降水)%s(%s%%)" % (rainfall, str(float(precip) * 100)), 32)
    sysgui.draw_string_center("湿度:%s %s风:%s(%s)" % (humidity, wind_direction, wind_scale, wind_speed), 48)

def draw_suggest():
    if global_var.get('weather_suggestion'):
        sysgui.draw_string_center("今日建议", 0)
        sysgui.draw_string_center(('穿衣指数 : ' + str(global_var['weather_suggestion']["results"][0]["suggestion"]["dressing"]["brief"])), 16)
        sysgui.draw_string_center(('运动指数 : ' + str(global_var['weather_suggestion']["results"][0]["suggestion"]["sport"]["brief"])), 32)
        sysgui.draw_string_center(('紫外线指数 : ' + str(global_var['weather_suggestion']["results"][0]["suggestion"]["uv"]["brief"])), 48)
    else:
        sysgui.draw_string_center("今日建议", 0)
        sysgui.draw_string_center("暂时没有建议", 16)

def draw_error():
    sysgui.draw_string_center("▲获取天气失败▲", 0)
    sysgui.draw_string_center("连接WIFI后", 16)
    sysgui.draw_string_center("再过来看看吧", 32)
    sysgui.draw_string_center("/ㄒoㄒ/~~", 48)

def get_weather():

    sysgui.tipBox("正在获取预报天气......")
    dailyResult = urequests.get(URL_DAILY_WEATHER_API + "&location=" + configData.read("weather", "location", "ip"))
    dailyRsp = dailyResult.json()
    if dailyResult.status_code != 200:
        dailyRsp = None
    dailyResult.close()
    sysgui.tipBox("正在获取此刻天气......")
    nowResult = urequests.get(URL_NOW_WEATHER_API + "&location=" + configData.read("weather", "location", "ip"))
    nowRsp = nowResult.json()
    if nowResult.status_code != 200:
        nowRsp = None
    nowResult.close()
    sysgui.tipBox("正在获取天气建议......")
    suggestionResult = urequests.get(URL_SUGGESTION_WEATHER_API + "&location=" + configData.read("weather", "location", "ip"))
    suggestionRsp = suggestionResult.json()
    if suggestionResult.status_code != 200:
        nowRsp = None
    suggestionResult.close()

    
    global_var['daily_weather'] = dailyRsp
    global_var['now_weather'] = nowRsp
    global_var['weather_suggestion'] = suggestionRsp
    global_var['daily_weather_time'] = time.time()
    

