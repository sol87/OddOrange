#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/25'
# version     :
# usage       :
# notes       :

# Built-in modules
import logging

# Third-party modules
from pymel.core import *

# Studio modules
from qtkit.odd_progress_dialog import odd_progress_dialog

# Local modules


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class OOTimeWarper(object):

    def create_time_warper(self, inputs=()):
        # 限制输出类型
        if not (isinstance(inputs, list) or isinstance(inputs, tuple)):
            log.error("TypeError: Invalid arguments for input. Excepted list, got {type}".format(
                type=type(inputs)))
        # 创建时间包裹
        time_warper = createNode("animCurveTL", name="time_warper1")
        time_warper.addAttr('isTimeWarper', k=0, h=1)
        min_time = playbackOptions(query=True, min=True)
        max_time = playbackOptions(query=True, max=True)
        time_warper.addKey(time=min_time, value=min_time)
        time_warper.addKey(time=max_time, value=max_time)
        keyTangent(time_warper, inTangentType="linear",
                   outTangentType="linear")
        # 连接属性
        self.connect_warper(time_warper, inputs)
        return time_warper

    def warper_act(self, time_warper, inputs, mode="connect"):
        if not objExists(time_warper):
            return
        # 复制warper，以防打断连接时warper被自动删除
        time_warper_duplicate = duplicate(time_warper)[0]
        # 遍历输入
        progress_dialog = odd_progress_dialog(len(inputs), "正在处理连接...")
        progress_dialog.show()
        current_num = 0
        for input in inputs:
            node = PyNode(input)
            # 如果类型为属性,打断与time_warper连接
            if type(node) == Attribute:
                self.attr_warper_act(time_warper, node, mode)
            else:
                # 如果类型不为属性,打断与time_warper连接
                for attr in node.listAttr(keyable=True, connectable=True):
                    self.attr_warper_act(time_warper, attr, mode)
            progress_dialog.setValue(current_num)
            current_num += 1
        # 清除复制的warper
        if objExists(time_warper):
            delete(time_warper_duplicate)
        else:
            time_warper_duplicate.rename(time_warper)

    def attr_warper_act(self, time_warper, attr, mode="connect"):
        """连接或打断属性与warper之间的关系"""
        time_warper = PyNode(time_warper)
        try:
            anim_cv = attr.inputs(type="animCurve")
        except Exception, e:
            log.warning("{}".format(e))
        else:
            if anim_cv:
                if mode == "disconnect":
                    uttc_node = anim_cv[0].inputs(type="unitToTimeConversion")
                    anim_cv[0].input.disconnect()
                    delete(uttc_node)
                elif mode == "connect":
                    time_warper.output >> anim_cv[0].input

    def connect_warper(self, time_warper, inputs):
        self.warper_act(time_warper, inputs, "connect")

    def disconnect_warper(self, time_warper, inputs):
        self.warper_act(time_warper, inputs, "disconnect")

    def breakdown_all(self, time_warper):
        # 打断全部链接
        time_warper = PyNode(time_warper)
        uttc_node = time_warper.outputs(type="unitToTimeConversion")
        time_warper.output.disconnect()
        delete(uttc_node)

    def list_time_warpers(self, mode="all"):
        if mode == "all":
            return [i for i in ls(type="animCurveTL") if i.hasAttr("isTimeWarper")]
        elif mode == "selected":
            return [i for i in selected(type="animCurveTL") if i.hasAttr("isTimeWarper")]
        else:
            log.error("ValueError: mode must be 'all' or 'selected'.")
