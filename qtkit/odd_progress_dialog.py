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

# Third-party modules
try:
    import PyQt4.QtCore as QtCore
    import PyQt4.QtGui as QtGui
except ImportError:
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui

# Studio modules

# Local modules


QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))


def odd_progress_dialog(num, info="处理中..."):
    """

    :param num: range max
    :param info: shown information
    :return: QProgressDialog
    """
    progress_dialog = QtGui.QProgressDialog()
    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
    progress_dialog.setMinimumDuration(5)
    progress_dialog.setWindowTitle(progress_dialog.tr("请等待"))
    progress_dialog.setLabelText(progress_dialog.tr(info))
    progress_dialog.setCancelButtonText(progress_dialog.tr("取消"))
    progress_dialog.setRange(0, num)
    return progress_dialog
