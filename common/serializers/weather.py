#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: weather
@time: 2023-04-07 13:44
description:  
"""
import os
import json
import requests
from django.conf import settings

# 定义常量
APP_ID = "27537238"
APP_SECRET = "9gKJwjvU"

WEATHER_DATA_FILE = os.path.join(settings.MEDIA_ROOT, 'common/weather.json')


def set_weather(city="杭州"):
    '''天气任务'''
    # 请求天气数据
    url = f"https://www.yiketianqi.com/free/day?appid={APP_ID}&appsecret={APP_SECRET}&unescape=1&city={city}"
    print(url)
    resp = requests.get(url)
    # 解析天气数据
    result = resp.json()
    print(result)
    with open(WEATHER_DATA_FILE, 'w') as f:
        json.dump(result, f)


def get_weather():
    '''读取天气文件'''
    if not os.path.exists(WEATHER_DATA_FILE):
        set_weather()
    with open(WEATHER_DATA_FILE, 'r') as f:
        data = json.load(f)
        return data
