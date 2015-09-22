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
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

# Studio modules

# Local modules


QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("gbk"))


def odd_progress_dlg(num, info="处理中..."):
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
