#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/8/6'
# version     :
# usage       :
# notes       :

# Built-in modules
from types import MethodType

# Third-party modules
from PyQt4 import QtCore

# Studio modules

# Local modules


left_click_count = right_click_count = 0


def implant_clicked_signal(obj, cmd, button="left"):
    """
    add a mousePressEvent to a QWidget Dynamically.
    :param obj: QObject
    :param cmd: function or command
    :param button: string. must be one of "left","right","doubleLeft","doubleRight"
    """

    if button not in ["left", "right", "doubleLeft", "doubleRight"]:
        raise ValueError('param "button" must be one of "left","right","doubleLeft","doubleRight"')

    timer = QtCore.QTimer()
    timer.setInterval(250)
    timer.setSingleShot(True)

    def __timeout():
        """
        assist the "mousePressEvent" method execute the command.
        """
        global left_click_count, right_click_count

        if left_click_count >= right_click_count:
            if left_click_count == 1:
                if button == "left": cmd()
            else:
                if button == "doubleLeft": cmd()
        else:
            if right_click_count == 1:
                if button == "right": cmd()
            else:
                if button == "doubleRight": cmd()
        left_click_count = right_click_count = 0

    timer.timeout.connect(__timeout)

    def mousePressEvent(obj, event):
        """
        Qt mousePressEvent,use a timer to judge how the button been clicked.
        :param obj: QObject
        :param event: QtEvent
        """
        global left_click_count, right_click_count

        if event.button() == QtCore.Qt.LeftButton:
            left_click_count += 1
            if not timer.isActive():
                timer.start()
        if event.button() == QtCore.Qt.RightButton:
            right_click_count += 1
            if not timer.isActive():
                timer.start()

    base_class = obj.__class__

    event = MethodType(mousePressEvent, obj, base_class)
    setattr(obj, "mousePressEvent", event)