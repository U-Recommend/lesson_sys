#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: tasks
@time: 2023-04-07 13:42
description:  
"""
from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from common.serializers.weather import set_weather
from common.utils import logger


@periodic_task(crontab(hour='*/1'))
def weather_tasks():
    '''天气任务'''
    logger.info("天气任务")
    set_weather()
