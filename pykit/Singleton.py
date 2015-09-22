#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/22'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules

# Studio modules

# Local modules


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == "__main__":
    class Logger(object):
        __metaclass__ = Singleton
