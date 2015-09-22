#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/21'
# version     :
# usage       :
# notes       :

# Built-in modules
import os

# Third-party modules

# Studio modules

# Local modules


def lock_file(path):
    os.system(r"attrib +r %s" % path)
