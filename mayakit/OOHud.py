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
import time

# Third-party modules
from pymel.core import *

# Studio modules
import pykit

# Local modules


class OOHud(object):
    __metaclass__ = pykit.Singleton

    def __init__(self, user_name='unnamed', lan="zh_cn"):
        self.__user_name = user_name
        self.__language = lan

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, value):
        if not isinstance(value, basestring):
            raise ValueError("user_name must be a string.")
        self.__user_name = value

    @property
    def language(self):
        return self.language

    @language.setter
    def language(self, value):
        if value not in ["zh_cn", "en_us"]:
            raise ValueError("laguage must be 'zh_cn' or 'en_us'")
        self.__language = value

    def clear(self):
        # ----clear all huds---- #
        all_huds = headsUpDisplay(lh=1)
        for HUD in all_huds:
            headsUpDisplay(HUD, e=1, vis=0)
        if headsUpDisplay('ww_fileName', ex=1):
            headsUpDisplay('ww_fileName', rem=1)
        if headsUpDisplay('ww_timeLabel', ex=1):
            headsUpDisplay('ww_timeLabel', rem=1)
        if headsUpDisplay('ww_nameLabel', ex=1):
            headsUpDisplay('ww_nameLabel', rem=1)
        if headsUpDisplay('ww_focalLabel', ex=1):
            headsUpDisplay('ww_focalLabel', rem=1)
        # ----turn off built in huds---- #
        mel.eval("setCameraNamesVisibility(0)")
        mel.eval("setCurrentFrameVisibility(0)")
        # ----clear refresh expression---- #
        if objExists("hudRefresh*"):
            delete("hudRefresh")

    def show(self):
        # ----clear old huds---- #
        self.clear()
        # ----format now time---- #
        if self.__language == "zh_cn":
            ctime = time.strftime(u"%Y/%m/%d 周{%a} %H:%M".encode('gbk'))
            now_time = ctime.format(Mon=ur"一".encode('gbk'),
                                    Tue=ur"二".encode('gbk'),
                                    Wed=ur"三".encode('gbk'),
                                    Thu=ur"四".encode('gbk'),
                                    Fri=ur"五".encode('gbk'),
                                    Sat=ur"六".encode('gbk'),
                                    Sun=ur"日".encode('gbk'))
        else:
            now_time = time.strftime("%Y/%m/%d %a %H:%M")
        # ----init huds---- #
        nfb0 = headsUpDisplay(nextFreeBlock=0)
        nfb4 = headsUpDisplay(nextFreeBlock=4)
        nfb5 = headsUpDisplay(nextFreeBlock=5)
        nfb6 = headsUpDisplay(nextFreeBlock=6)
        # ----create huds---- #
        headsUpDisplay('ww_fileName', section=0, block=nfb0,
                       c="import maya_ctrls;maya_ctrls.get_scene_name()", event="NewSceneOpened",
                       lfs="large", dfs="large")
        headsUpDisplay('ww_timeLabel', section=5, block=nfb5,
                       c='"%s"' % now_time,
                       lfs="large", dfs="large")
        headsUpDisplay('ww_nameLabel', section=6, block=nfb6,
                       c='"%s"' % self.__user_name,
                       lfs="large", dfs="large")
        headsUpDisplay('ww_focalLabel', section=4, block=nfb4,
                       c="import maya_ctrls;maya_ctrls.get_current_cam_fl()", event="timeChanged",
                       lfs="large", dfs="large")
        # ----turn on built in huds---- #
        mel.eval("setCameraNamesVisibility(1)")
        mel.eval("setCurrentFrameVisibility(1)")

        # ---- create a expression to refresh hud---- #
        expression(n="hudRefresh",
                   s="python(\"import maya.cmds as mc;mc.headsUpDisplay('ww_focalLabel', refresh=1)\")",
                   o="", ae=1, uc="all")
