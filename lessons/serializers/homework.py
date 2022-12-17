#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: lession
@time: 2022-11-04 23:39
description:  
"""
import sys
from io import StringIO
import contextlib
from lessons.models import Homework


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def homework_create_or_update(user_id, exercises_id, lesson_id, code=None, content=None):
    homework = Homework.objects.filter(user_id=user_id, exercises_id=exercises_id)
    if lesson_id:
        homework = homework.filter(lesson_id=lesson_id)
    homework = homework.first()
    if homework:
        homework.code = code
        homework.content = content
        homework.save()
    else:
        homework = Homework(user_id=user_id, lesson_id=lesson_id, exercises_id=exercises_id, code=code, content=content)
        homework.save()
    return homework
