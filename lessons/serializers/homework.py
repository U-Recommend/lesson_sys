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


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
