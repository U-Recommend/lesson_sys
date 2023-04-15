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
import time
import requests
from django.conf import settings
from common.utils import logger

# 定义常量
APP_ID = "27537238"
APP_SECRET = "9gKJwjvU"

WEATHER_DATA_FILE = os.path.join(settings.MEDIA_ROOT, 'common/weather.json')


def set_weather(city="杭州"):
    '''天气任务'''
    # 请求天气数据
    url = f"https://www.yiketianqi.com/free/day?appid={APP_ID}&appsecret={APP_SECRET}&unescape=1&city={city}"
    logger.info(url)
    resp = requests.get(url)
    # 解析天气数据
    result = resp.json()
    logger.info(result)
    result['now'] = int(time.time())
    with open(WEATHER_DATA_FILE, 'w') as f:
        json.dump(result, f)
    return result


def get_weather():
    '''读取天气文件'''
    with open(WEATHER_DATA_FILE, 'r') as f:
        data = json.load(f)
        logger.info(data)
        if not data.get('city'):
            data = {
                "nums": 226,  # 今日实时请求次数
                "cityid": "101120101",  # 城市ID
                "city": "济南",
                "date": "2022-05-05",
                "week": "星期四",
                "update_time": "22:38",  # 更新时间
                "wea": "多云",  # 天气情况
                "wea_img": "yun",  # 天气标识
                "tem": "25",  # 实况温度
                "tem_day": "30",  # 白天温度(高温)
                "tem_night": "23",  # 夜间温度(低温)
                "win": "南风",  # 风向
                "win_speed": "3级",  # 风力
                "win_meter": "19km\/h",  # 风速
                "air": "53",  # 空气质量
                "pressure": "987",  # 气压
                "humidity": "27%"  # 湿度
            }
        org_now = data.get('now', 0)
        now = int(time.time())
        delta = (now - int(org_now)) / (60 * 60)
        logger.info(delta)
        if delta < 1:
            logger.info('ddddd')
            return data
        data = set_weather()
        return data
