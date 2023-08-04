#!/usr/bin/python
# encoding: utf-8

"""
@author: tonytan
@file: website
@time: 2023-01-03 14:51
description:  
"""

from website.models import Website


def website_first():
    website = Website.objects.first()
    return website
