#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/23'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
import maya.OpenMaya as openmaya
import PyQt4.QtCore as QtCore

# Studio modules

# Local modules


class MayaSelectWatcher(QtCore.QObject):
    # 单例
    current_instance = None

    # 信号
    something_selected = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(MayaSelectWatcher, self).__init__(*args, **kwargs)
        if self.current_instance:
            raise Exception("A MayaSelectedWatcher object already exists.")

        # 创建条件捕捉对象
        self.event_message = openmaya.MEventMessage()
        self.event_message.addEventCallback("SelectionChanged", self.on_something_selected)
        MayaSelectWatcher.current_instance = self

    def __del__(self):
        MayaSelectWatcher.current_instance = None

    def __get_selected_list(self):
        nodes = []
        sel_list = openmaya.MSelectionList()
        openmaya.MGlobal.getActiveSelectionList(sel_list)
        sel_list.getSelectionStrings(nodes)
        return nodes

    def on_something_selected(self, *args):
        selected_nodes = self.__get_selected_list()
        self.something_selected.emit(selected_nodes)

    @classmethod
    def get_select_watcher(cls):
        return cls.current_instance


if __name__ == "__main__":
    watcher = MayaSelectWatcher.get_select_watcher()
    if not watcher:
        watcher = MayaSelectWatcher()

    def foo(*arg):
        print arg
    watcher.something_selected.connect(foo)

