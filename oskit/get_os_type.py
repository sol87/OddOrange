#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/7/24'
# version     :
# usage       :
# notes       :

# Built-in modules
import sys

# Third-party modules

# Studio modules

# Local modules


def get_os_type():
    """
    Return the type of current operation system like "windows" "osx" or "Linux"
    :return os_type: string
    """

    if sys.platform.startswith("win"):
        os_type = "windows"
    elif sys.platform.startswith("linux"):
        os_type = "linux"
    else:
        os_type = "osx"
    return os_type
