#!/usr/bin/python
# encoding: utf-8

"""
@author: rainsty
@file:   test.py
@time:   2019-07-08 17:08
@description:
"""

from src.common.dirtyWordOfFilter import DFAFilter
f = DFAFilter()
text = "傻b"
result = f.filter(text)
print(result)
