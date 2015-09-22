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
import get_md5

# Third-party modules

# Studio modules

# Local modules


def compile_files(first_file, sec_file):
    if os.path.isfile(first_file) and os.path.isfile(sec_file):
        if get_md5.get_md5(first_file) == get_md5.get_md5(sec_file):
            return True
        return False
    raise ValueError("not a exist file.")
