#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 15:12
# @Author  : nieyuwei

import os
from smart_open import smart_open


class MyReader(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        if os.path.isdir(self.dirname):
            for fname in os.listdir(self.dirname):
                if os.path.isfile(os.path.join(self.dirname, fname)):
                    for line in smart_open(os.path.join(self.dirname, fname), 'r'):
                        yield line.strip().split()
        else:
            if os.path.isfile(self.dirname):
                for line in smart_open(self.dirname, 'r'):
                    yield line.strip().split()
