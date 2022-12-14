#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: knowledge
@time: 2022-12-11 15:39
description:  
"""

from knowledges.models import Knowledge


def knowledge_filter(id=None, language=None):
    query = Knowledge.objects.filter(is_deleted=0)
    if id:
        query = query.filter(id=id)
    if language:
        query = query.filter(language=language)
    return query.order_by("sort")


def knowledge_data(knowledge=None):
    data = {
        "id": knowledge.id,
        "language": knowledge.language,
        'title': knowledge.title,
        'parent_id': knowledge.parent_id
    }
    return data
