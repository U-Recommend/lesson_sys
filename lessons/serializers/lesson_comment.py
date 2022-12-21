#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: lesson_comment
@time: 2022-12-21 10:11
description:  
"""
from lessons.models import LessonComment


def lesson_comment_filter(uid=None, lid=None, hid=None, pid=None, id=None):
    query = LessonComment.objects.filter(is_deleted=0)
    if id:
        query = query.filter(id=id)
    if uid:
        query = query.filter(user_id=uid)
    if lid:
        query = query.filter(lesson_id=lid)
    if hid:
        query = query.filter(homework_id=hid)
    if pid:
        query = query.filter(parent_id=pid)
    return query.order_by('-id')


def lesson_comment_data(comment=None):
    user = comment.user
    lesson = comment.lesson
    homework = comment.homework
    data = {
        'id': comment.id,
        'content': comment.content or '',
        'parent_id': comment.parent.id if comment.parent else "",
        'user_id': user.id,
        'user_name': user.name,
    }
    return data
