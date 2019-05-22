#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 15:12
# @Author  : nieyuwei

import os
import sys
import itertools
import random
import smart_open

if sys.version_info[0] >= 3:
    unicode = str


class MyReader(object):
    def __init__(self, dirname, sep=" "):
        self.dirname = dirname
        self.sep = sep

    def __iter__(self):
        if os.path.isdir(self.dirname):
            for fname in os.listdir(self.dirname):
                if os.path.isfile(os.path.join(self.dirname, fname)):
                    for line in smart_open.open(os.path.join(self.dirname, fname), 'r'):
                        yield line.strip().split(sep=self.sep)
        else:
            if os.path.isfile(self.dirname):
                for line in smart_open.open(self.dirname, 'r'):
                    yield line.strip().split(sep=self.sep)


def chunks(l, size):
    """Divide a list in chunks"""
    lst = list(l)
    random.shuffle(lst)
    l_c = iter(lst)
    while 1:
        x = tuple(itertools.islice(l_c, size))
        if not x:
            return
        yield x


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def any2utf8(text, errors='strict', encoding='utf8'):
    """Convert a unicode or bytes string in the given encoding into a utf8 bytestring.

    Parameters
    ----------
    text : str
        Input text.
    errors : str, optional
        Error handling behaviour if `text` is a bytestring.
    encoding : str, optional
        Encoding of `text` if it is a bytestring.

    Returns
    -------
    str
        Bytestring in utf8.

    """

    if isinstance(text, unicode):
        return text.encode('utf8')
    # do bytestring -> unicode -> utf8 full circle, to ensure valid utf8
    return unicode(text, encoding, errors=errors).encode('utf8')