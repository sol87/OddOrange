#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :''
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
try:
    import PyQt4.QtCore as QtCore
except ImportError:
    import PySide.QtCore as QtCore

# Studio modules

# Local modules


def drag_move_dec(widget_class):
    """
    A decorator offers drag and move event functions for a qwidget class
    :param widget_class: QObject
    :return MovedClass: QObject
    """

    class MovedClass(widget_class):
        def __init__(self, *args, **kwargs):
            super(MovedClass, self).__init__(*args, **kwargs)
            self.wrapped = widget_class()
            self.__last_clicked_pos = None

        @property
        def last_clicked_pos(self):
            return self.__last_clicked_pos

        def mousePressEvent(self, event):
            super(MovedClass, self).mousePressEvent(event)
            self.__last_clicked_pos = (event.globalPos(), QtCore.QPoint(self.pos()))

        def mouseMoveEvent(self, event):
            if self.__last_clicked_pos:
                move, begin = self.__last_clicked_pos
                self.move((event.globalPos()-move)+begin)
            else:
                super(MovedClass, self).mouseMoveEvent(event)

        def mouseReleaseEvent(self, event):
            super(MovedClass, self).mouseReleaseEvent(event)
            self.__last_clicked_pos = None

    return MovedClass

if __name__ == "__main__":
    import PyQt4.QtGui as QtGui
    import sys

    @drag_move_dec
    class TestLabel(QtGui.QLabel):
        pass

    app = QtGui.QApplication(sys.argv)
    test = TestLabel("hello")
    test.show()
    app.exec_()
