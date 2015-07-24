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

# Third-party modules

# Studio modules

# Local modules


def singleton_dec(widget_class):
    """
    A decorator makes target widget singleton
    :param widget_class: QObject
    :return MovedClass: QObject
    """

    class SingletonClass(widget_class):
        instances = []

        def __init__(self, *args, **kwargs):
            super(SingletonClass, self).__init__(*args, **kwargs)
            for obj in SingletonClass.instances:
                obj.deleteLater()
            SingletonClass.instances.append(self)

    return SingletonClass

if __name__ == "__main__":
    import PyQt4.QtGui as QtGui
    import sys

    @singleton_dec
    class TestLabel(QtGui.QLabel):
        pass

    app = QtGui.QApplication(sys.argv)
    test1 = TestLabel("hello")
    test1.show()
    test2 = TestLabel("yes")
    test2.show()
    test3 = TestLabel("nihao")
    test3.show()
    app.exec_()
