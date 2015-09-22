#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

all_modules = [os.path.splitext(i)[0] for i in os.listdir(os.path.split(__file__)[0]) if i.endswith(".py") and i != "__init__.py"]
for module_name in all_modules:
    exec("from {0} import {0}".format(module_name))

# add parent path to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir) 