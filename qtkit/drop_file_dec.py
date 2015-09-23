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
    Signal = QtCore.pyqtSignal
except ImportError:
    import PySide.QtCore as QtCore
    Signal = QtCore.Signal

# Studio modules

# Local modules


def drop_file_dec(widget_class):
    """
    A decorator offers drop file event functions for a qwidget class
    :param widget_class: QObject
    :return MovedClass: QObject
    """

    class DropClass(widget_class):
        droped_in = Signal(list)

        def __init__(self, *args, **kwargs):
            super(DropClass, self).__init__(*args, **kwargs)
            self.setAcceptDrops(True)
            self.wrapped = widget_class()

        def dragEnterEvent(self, event):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
            else:
                event.ignore()

        def dragMoveEvent(self, event):
            if event.mimeData().hasUrls:
                event.acceptProposedAction()
            else:
                event.ignore()

        def dropEvent(self, event):
            in_paths = list()
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                in_paths.append(path)
            self.droped_in.emit(in_paths)

    return DropClass

if __name__ == "__main__":
    import PyQt4.QtGui as QtGui
    import sys

    @drop_file_dec
    class TestLabel(QtGui.QLabel):
        pass

    def print_files(file_list):
        print "="*20
        for f in file_list:
            print unicode(f)
        print "="*20

    app = QtGui.QApplication(sys.argv)
    test = TestLabel("hello")
    test.droped_in.connect(print_files)
    test.show()
    app.exec_()
