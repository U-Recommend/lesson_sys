#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: exercises
@time: 2022-11-25 00:07
description:  
"""
from common.models import STATUS
from lessons.models import Exercises, Homework


def exercises_filter(id=None, status=None):
    query = Exercises.objects.filter(is_deleted=0)
    if id:
        query = query.filter(id=id)
    if str(status) in [str(i[0]) for i in STATUS]:
        query = query.filter(status=status)
    return query


def exercises_first(eid=None, exercises=None):
    if id:
        return exercises_filter(id=eid).first()
    return exercises


def exercises_data(eid=None, exercises=None, uid=None, lesson_id=None):
    exercises = exercises_first(eid=eid, exercises=exercises)
    if not exercises:
        return {}
    items = ('id', 'code_language', 'title', 'content', 'default_code', 'need_code', 'need_answer', 'code', 'status')
    data = {item: getattr(exercises, item, '') for item in items}
    data['comment'] = ''
    data['homework_content'] = ''
    homework = None
    if uid:
        homework = Homework.objects.filter(user_id=uid, exercises_id=exercises.id,
                                           is_deleted=0)
        if lesson_id:
            homework = homework.filter(lesson_id=lesson_id)
        homework = homework.first()
    if homework:
        if homework.code:
            data['default_code'] = homework.code or ""
            data['homework_content'] = homework.content or ""
        if homework.comment:
            data['comment'] = homework.comment
    return data
