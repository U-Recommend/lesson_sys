#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: attendance
@time: 2022-12-03 16:35
description:  
"""
from common.utils import logger
from lessons.serializers.lesson import lesson_filter


def attendance_data(lesson=None, user=None):
    data = {
        'date': lesson.lesson_date.strftime("%Y-%m-%d"),
        'lesson_id': lesson.id,
        'lesson_name': lesson.course.title,
    }
    logger.info(data)
    return data
