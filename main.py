from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import urllib.parse

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://wttr.in/" + urllib.parse.quote(city) + "?format=j1"
  res = requests.get(url).json()
  current = res['current_condition'][0]
  code = int(current['weatherCode'])
  temp = int(current['temp_C'])
  today_forecast = res['weather'][0]
  high = int(today_forecast['maxtempC'])
  low = int(today_forecast['mintempC'])

  # 用国际标准的weatherCode做映射
  weather_map = {
    113: "晴", 116: "多云", 119: "阴", 122: "阴",
    143: "雾", 176: "小雨", 179: "小雪",
    182: "雨夹雪", 185: "雨夹雪",
    200: "雷阵雨", 227: "暴风雪",
    230: "暴风雪", 248: "雾", 260: "雾",
    263: "小雨", 266: "小雨", 281: "雨夹雪",
    284: "雨夹雪", 293: "小雨", 296: "小雨",
    299: "中雨", 302: "中雨", 305: "大雨",
    308: "大雨", 311: "雨夹雪", 314: "雨夹雪",
    317: "雨夹雪", 320: "雨夹雪",
    323: "小雪", 326: "小雪", 329: "中雪",
    332: "中雪", 335: "大雪", 338: "大雪",
    350: "冰雹", 353: "小雨",
    362: "雨夹雪", 365: "雨夹雪",
    368: "小雪", 371: "大雪",
    374: "冰雹", 377: "冰雹",
    386: "雷阵雨", 389: "雷阵雨",
    392: "雷阵雨", 395: "大雪",
  }
weather_cn = weather_map.get(code, "未知")
weather_desc = weather_cn + "，" + str(low) + "~" + str(high) + "°C"
# 临时把情话塞进天气字段测试
weather_desc = weather_desc + "\n" + get_words()
return weather_desc, temp





def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  return "测试123"



def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
