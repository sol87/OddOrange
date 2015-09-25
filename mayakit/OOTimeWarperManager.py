#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/14'
# version     :
# usage       :
# notes       :

# Built-in modules
import logging
import re

# Third-party modules
from pymel.core import *
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

# Studio modules

# Local modules
from get_selected_channels import get_selected_channels
from OOTimeWarper import OOTimeWarper
from safe_to_string import safe_to_string


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

time_warper = OOTimeWarper()


class OOTimeWarperModel(QtCore.QAbstractListModel):

    def __init__(self, warpers=(), parent=None):
        super(OOTimeWarperModel, self).__init__(parent)
        self.__warper_list = warpers

    def flags(self, index):
        # 可编辑，可用，可选
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent):
        # 行数
        return len(self.__warper_list)

    def data(self, index, role):
        value = self.__warper_list[index.row()]
        # 显示内容
        if role == QtCore.Qt.DisplayRole:
            return value
        # 编辑时保持原值
        if role == QtCore.Qt.EditRole:
            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            # 列头
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("OOTimeWarper")
            # 行头
            else:
                return QtCore.QString("%1").arg(section)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            # 如果符合maya命名规范则设置
            if re.match(r'\D\w*', value):
                # 重命名曲线
                rename(self.__warper_list[row], value)
                # 修改Model内容
                self.__warper_list[row] = value
                # 刷新Model
                self.dataChanged.emit(index, index)
                return True
        return False

    def get_data_index(self, value):
        # 获取值在列表中的位置
        try:
            row = self.__warper_list.index(value)
            return self.index(row)
        except ValueError, e:
            log.warning("{}".format(e))
        return

    def update_warpers(self):
        # 列举所有warper节点
        all_warpers = time_warper.list_time_warpers()
        all_warpers_str = [i.name() for i in all_warpers]
        # 刷新列表
        self.__warper_list = all_warpers_str
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        return True


class OOTimeWarperManager(QtGui.QDialog):

    def __init__(self, parent=None):
        super(OOTimeWarperManager, self).__init__(parent)

        self.setWindowTitle("Time Warper Manager")
        self.main_layout = QtGui.QVBoxLayout(self)

        # 增删按钮组
        # -创建按钮组layout
        self.warper_buttons_layout = QtGui.QHBoxLayout()
        # -创建按钮
        self.create_button = QtGui.QPushButton()
        self.create_button.setText("Create")
        self.remove_button = QtGui.QPushButton()
        self.remove_button.setText("Remove")
        self.clear_button = QtGui.QPushButton()
        self.clear_button.setText("Clear")
        self.refresh_button = QtGui.QPushButton()
        self.refresh_button.setText("Refresh")
        # -布局按钮
        self.warper_buttons_layout.addWidget(self.create_button)
        self.warper_buttons_layout.addWidget(self.remove_button)
        self.warper_buttons_layout.addWidget(self.clear_button)
        self.warper_buttons_layout.addWidget(self.refresh_button)
        self.main_layout.addLayout(self.warper_buttons_layout)
        # -连接按钮功能
        self.create_button.clicked.connect(self.on_create_button_clicked)
        self.remove_button.clicked.connect(self.on_remove_button_clicked)
        self.clear_button.clicked.connect(self.on_clear_button_clicked)
        self.refresh_button.clicked.connect(self.update_selection)

        # 主listView
        # -创建listView
        self.warper_model = OOTimeWarperModel()
        self.warper_list_view = QtGui.QListView()
        self.warper_list_view.setModel(self.warper_model)
        self.warper_list_view.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.main_layout.addWidget(self.warper_list_view)
        self.select_model = self.warper_list_view.selectionModel()
        # -设置Model
        self.warper_model.update_warpers()
        # -连接切换选择信号
        self.select_model.selectionChanged.connect(self.on_selection_changed)

        # 连接按钮组
        # -创建按钮组layout
        self.connect_buttons_layout = QtGui.QHBoxLayout()
        # -创建按钮
        self.connect_button = QtGui.QPushButton()
        self.connect_button.setText("Connect")
        self.disconnect_button = QtGui.QPushButton()
        self.disconnect_button.setText("Disconnect")
        self.attr_link_button = QtGui.QPushButton()
        self.attr_link_button.setText("Attr Link +")
        self.brk_link_button = QtGui.QPushButton()
        self.brk_link_button.setText("Attr Link -")
        # -布局按钮
        self.connect_buttons_layout.addWidget(self.connect_button)
        self.connect_buttons_layout.addWidget(self.disconnect_button)
        self.connect_buttons_layout.addWidget(self.attr_link_button)
        self.connect_buttons_layout.addWidget(self.brk_link_button)
        self.main_layout.addLayout(self.connect_buttons_layout)
        # -连接按钮功能
        self.connect_button.clicked.connect(self.on_connect_button_clicked)
        self.disconnect_button.clicked.connect(self.on_disconn_button_clicked)
        self.attr_link_button.clicked.connect(self.on_attr_link_button_clicked)
        self.brk_link_button.clicked.connect(self.on_brk_link_button_clicked)

        # 刷新选中内容
        self.update_selection()

    def list_UI_selected_warper(self):
        # 获取UI中选中的warper
        selected_warpers = []
        selected_indexs = self.select_model.selectedIndexes()
        for index in selected_indexs:
            selected_warpers.append(index.data())
        return selected_warpers

    def update_selection(self):
        """刷新选中的warper"""
        # 刷新warpers
        self.warper_model.update_warpers()
        # 清空选中列表
        self.select_model.clearSelection()
        # 获取选中的warper
        selected_warpers = self.list_UI_selected_warper()
        for warper in selected_warpers:
            # 获取warpers的index
            index = self.warper_model.get_data_index(warper)
            if index:
                # 选择对应item
                self.select_model.select(index, self.select_model.Select)

    def on_selection_changed(self, item_selection):
        """选中listView中行时，选中相应warper曲线。"""
        # 获取UI中选中的warper
        selected_warpers = self.list_UI_selected_warper()
        # 选中warper,设置开关防止陷入刷新死循环
        selected_warpers = [safe_to_string(i.toString()) for i in selected_warpers]
        select(selected_warpers)

    def on_create_button_clicked(self):
        """创建warper并连接到选中控制器已Key帧属性"""
        # 获取选中的控制器
        ctrls = [i for i in selected(dagObjects=True) if i in selected()]
        # 创建warper并连接到控制器已Key帧属性
        time_warper.create_time_warper(ctrls)
        # 刷新界面
        self.warper_model.update_warpers()

    def on_remove_button_clicked(self):
        """删除选中的warper"""
        # 获取选中warper
        selected_warpers = self.list_UI_selected_warper()
        selected_warpers = [safe_to_string(i.toString()) for i in selected_warpers]
        # 删除
        delete(selected_warpers)
        # 刷新界面
        self.warper_model.update_warpers()

    def on_clear_button_clicked(self):
        """删除所有warper"""
        # 获取选中warper
        all_warpers = time_warper.list_time_warpers()
        # 删除
        delete(all_warpers)
        # 刷新界面
        self.warper_model.update_warpers()

    def on_connect_button_clicked(self):
        """建立选中控制器的已Key属性与选中warper之间连接"""
        # 获取选中的控制器
        ctrls = [i for i in selected(dagObjects=True) if i in selected()]
        # 获取选中warpers
        selected_warpers = self.list_UI_selected_warper()
        selected_warpers = [safe_to_string(i.toString()) for i in selected_warpers]
        # 连接属性
        for warper in selected_warpers:
            time_warper.connect_warper(warper, ctrls)

    def on_disconn_button_clicked(self):
        """打断选中控制器与选中warper之间连接"""
        # 获取选中的控制器
        ctrls = [i for i in selected(dagObjects=True) if i in selected()]
        # 获取选中warpers
        selected_warpers = self.list_UI_selected_warper()
        selected_warpers = [safe_to_string(i.toString()) for i in selected_warpers]
        # 连接属性
        for warper in selected_warpers:
            if not ctrls:
                time_warper.breakdown_all(warper)
            else:
                time_warper.disconnect_warper(warper, ctrls)

    def on_attr_link_button_clicked(self):
        """建立选中的已Key属性与warper之间连接"""
        # 获取选中属性
        selected_attrs = []
        selected_objs = [i for i in selected(
            dagObjects=True) if i in selected()]
        selected_channels = get_selected_channels()
        for obj in selected_objs:
            selected_attrs.extend(["{obj}.{attr}".format(
                obj=obj, attr=i) for i in selected_channels])
        # 获取选中warpers
        selected_warpers = self.list_UI_selected_warper()
        selected_warpers = [safe_to_string(i.toString()) for i in selected_warpers]
        # 连接属性
        if selected_attrs and selected_warpers:
            for warper in selected_warpers:
                time_warper.connect_warper(warper, selected_attrs)

    def on_brk_link_button_clicked(self):
        """打断选中的已Key属性与warper之间连接"""
        # 获取选中属性
        selected_attrs = []
        selected_objs = [i for i in selected(
            dagObjects=True) if i in selected()]
        selected_channels = get_selected_channels()
        for obj in selected_objs:
            selected_attrs.extend(["{obj}.{attr}".format(
                obj=obj, attr=i) for i in selected_channels])
        # 获取选中warpers
        selected_warpers = self.list_UI_selected_warper()
        selected_warpers = [safe_to_string(i.toString()) for i in selected_warpers]
        # 打断连接
        if selected_attrs and selected_warpers:
            for warper in selected_warpers:
                time_warper.disconnect_warper(warper, selected_attrs)

if __name__ == "__main__":
    import mayakit
    maya_win = mayakit.get_maya_win("PyQt4")
    twm = OOTimeWarperManager(maya_win)
    twm.show()
