#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: feedback
@time: 2022-12-20 16:43
description:  
"""

from common.models import Feedback
from common.serializers.user import user_data


def feedback_filter(id=None, is_private=None, uid=None):
    query = Feedback.objects.filter(is_deleted=0)
    if id:
        query = query.filter(id=id)
    if is_private:
        query = query.filter(is_private=is_private)
    if uid:
        query = query.filter(user_id=uid)
    return query


def feedback_data(feedback=None, feedback_id=None):
    if feedback_id:
        feedback = feedback_filter(id=feedback_id).first()
    if not feedback:
        return {}
    user = user_data(user=feedback.user)
    data = {
        'id': feedback.id,
        'user': user,
        'content': feedback.content or '',
        'is_private': feedback.is_private,
        'is_private_name': feedback.get_is_private_display(),
        'feedback': feedback.feedback or '',
        'status': feedback.status,
        'created': feedback.created.strftime("%Y年%m月%d日 %S点%M分"),
        'user_name': user.get('name', ''),
        'user_id': feedback.user_id,
    }
    return data
