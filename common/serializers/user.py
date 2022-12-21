#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: user
@time: 2022-12-20 16:46
description:  
"""
from common.models import Grade, User


def user_data(user=None):
    data = {
        'id': user.id,
        'name': user.name or ''
    }
    return data
