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
import zipfile

# Third-party modules

# Studio modules

# Local modules


def unzip(zip_file, target_path="D:/"):
    f = zipfile.ZipFile(zip_file, 'r')  
    for file_name in f.namelist():
        f.extract(file_name, target_path)