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
  love_words = [
    "🌈 琳琳宝贝，你是上天派来拯救我平庸生活的仙女",
    "老婆 💫 这个世界上最美的风景，就是每天醒来想到你❤️",
    "✨媳妇儿，所有的好运都用来遇见你了 ❤️",
    "❤️ 刘文秀同学，遇见你是我这辈子最幸运的事",
    "仙女宝宝 ✨ 今天的风很温柔，但不及你的万分之一🌸",
    "琳琳，你知道吗 ❤️ 你是我所有失眠夜里唯一的甜",
    "超级无敌天下第一美的琳琳 ❤️ 今天也要狠狠爱你",
    "宝宝 ❤️ 遇见你之前我觉得世界很大，之后觉得你就是世界🌈",
    "🌈 媳妇儿，你的名字是我听过最短的情诗",
    "老婆大人 ❤️ 今天的你也一定是全世界最可爱的人",
    "🌈 仙女宝宝，我愿意用一生的时间换你每天的微笑🌈",
    "琳琳宝贝 ❤️ 你是我的日出，也是我的日落",
    "媳妇儿，想把你藏进我的口袋里 ❤️ 走到哪都带着",
    " 🌸 琳琳宝宝，你一笑我的整个世界都变成了粉色",
    "宝宝 ❤️ 这辈子最幸运的两件事，一件是遇见你，一件是和你并肩同行",
    "琳琳 🌸 你的名字念在嘴边，甜在心里",
    "超级无敌天下第一美的琳琳宝贝 ✨ 今天也是为你心动的一天",
    "🌈 媳妇儿，我想和你虚度时光，从日出到日落",
    "仙女宝宝，你是我疲惫生活里 ❤️ 唯一的光",
    "老婆 ✨ 时间很短人生很长，但有了你就刚刚好",
    "🌸 琳琳，喜欢你就像是夏天的冰可乐，舒服又自然",
    "媳妇儿，世界很大人生很长 💫 可我只想和你挤在一张沙发上",
    "宝宝 💫 你是我不经意间撞到的温柔，一撞就是一辈子",
    "🌸 宝贝，你是我见过的天下最漂亮的女孩子",
    "琳琳宝贝，所有的情话都不如 ✨ 你在我身边🌈",
    "🌈 媳妇儿你知道吗，我真的超级无敌爱你",
    "仙女宝宝，爱你这件事 ✨ 我从没想过要停下来",
    "老婆 ❤️ 你的存在就是我每天努力的全部理由",
    "琳琳 💫 永远和我在一起好么 我会永远宠你爱你",
    "超级无敌天下第一美的琳琳 🌸 我们的故事，才刚刚开始",
  ]
  return random.choice(love_words)


def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
