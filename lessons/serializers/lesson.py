#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: lesson
@time: 2022-12-03 16:37
description:  
"""

from common.models import STATUS
from lessons.models import Lesson


def lesson_filter(id=None, user=None, uid=None, status=None, course=None, cid=None):
    query = Lesson.objects.filter(is_deleted=0)
    if id:
        query = query.filter(id=id)
    if user:
        query = query.filter(user=user)
    if uid:
        query = query.filter(user_id=uid)
    if str(status) in [str(i) for i, _ in STATUS]:
        query = query.filter(status=status)
    if course:
        query = query.filter(course=course)
    if cid:
        query = query.filter(course_id=cid)
    return query
