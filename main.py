from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  import urllib.parse
  url = "https://wttr.in/" + urllib.parse.quote(city) + "?format=j1&lang=zh"
  res = requests.get(url).json()
  current = res['current_condition'][0]
  weather_en = current['weatherDesc'][0]['value']
  temp = int(current['temp_C'])
  today_forecast = res['weather'][0]
  high = int(today_forecast['maxtempC'])
  low = int(today_forecast['mintempC'])

  # 英文天气翻译成中文
  weather_map = {
    "Sunny": "晴", "Clear": "晴",
    "Partly cloudy": "多云", "Partly Cloudy": "多云",
    "Cloudy": "阴", "Overcast": "阴",
    "Mist": "薄雾", "Fog": "雾",
    "Light rain": "小雨", "Light drizzle": "小雨",
    "Patchy rain possible": "可能有阵雨",
    "Moderate rain": "中雨", "Heavy rain": "大雨",
    "Light snow": "小雪", "Moderate snow": "中雪",
    "Thunderstorm": "雷阵雨",
  }
  weather_cn = weather_map.get(weather_en, weather_en)
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
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
