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
import shutil

# Third-party modules

# Studio modules

# Local modules


def copy_file(src_path, tar_path):
    if os.path.isfile(src_path):
        tar_dir = os.path.dirname(tar_path)
        if not os.path.isdir(tar_dir):
            os.makedirs(tar_dir)
        shutil.copy(src_path, tar_path)
    elif os.path.isdir(src_path):
        shutil.copytree(src_path, tar_path)
    else:
        raise ValueError("%s is not a exist file." % src_path)
    return "copy %s to %s" % (src_path, tar_path)
