# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
import csv
import json
import os
from collections import OrderedDict

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem

from EventEngine import Event


def loadFont():
    """载入字体设置"""
    fileName = 'fc_setting.json'
    path = os.path.abspath(os.path.dirname(__file__))
    fileName = os.path.join(path, fileName)

    try:
        f = open(fileName)
        setting = json.load(f)
        family = setting['fontFamily']
        size = setting['fontSize']
        font = QtGui.QFont(family, size)
    except:
        font = QtGui.QFont('微软雅黑', 12)
    return font


BASIC_FONT = loadFont()


########################################################################
class BasicFcView(QTableWidget):
    """
    基础监控

    headerDict中的值对应的字典格式如下
    {'chinese': u'中文名', 'cellType': BasicCell}

    """
    # 定义信号
    signal = pyqtSignal(type(Event()))

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine=None, eventEngine=None, parent=None):
        """Constructor"""
        super(BasicFcView, self).__init__(parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # 保存表头标签用
        self.headerDict = OrderedDict()  # 有序字典，key是英文名，value是对应的配置字典
        self.headerList = []  # 对应self.headerDict.keys()

        # 保存相关数据用
        self.dataDict = {}  # 字典，key是字段对应的数据，value是保存相关单元格的字典
        self.dataKey = ''  # 字典键对应的数据字段

        # 监控的事件类型
        self.eventType = ''

        # 字体
        self.font = None

        # 保存数据对象到单元格
        self.saveData = False

        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = False

        # 初始化右键菜单
        self.initPopMenu()

    # ----------------------------------------------------------------------
    def setHeaderDict(self, headerDict):
        """设置表头有序字典"""
        self.headerDict = headerDict
        self.headerList = headerDict.keys()

    # ----------------------------------------------------------------------
    def setDataKey(self, dataKey):
        """设置数据字典的键"""
        self.dataKey = dataKey

    # ----------------------------------------------------------------------
    def setEventType(self, eventType):
        """设置监控的事件类型"""
        self.eventType = eventType

    # ----------------------------------------------------------------------
    def setFont(self, font):
        """设置字体"""
        self.font = font

    # ----------------------------------------------------------------------
    def setSaveData(self, saveData):
        """设置是否要保存数据到单元格"""
        self.saveData = saveData

    # ----------------------------------------------------------------------
    def initTable(self):
        """初始化表格"""
        # 设置表格的列数
        col = len(self.headerDict)
        self.setColumnCount(col)

        # 设置列表头
        labels = [d['chinese'] for d in self.headerDict.values()]
        self.setHorizontalHeaderLabels(labels)

        # 关闭左边的垂直表头
        self.verticalHeader().setVisible(False)

        # 设为不可编辑
        self.setEditTriggers(self.NoEditTriggers)

        # 设置表格自适应大小
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设为行交替颜色
        self.setAlternatingRowColors(True)

        # 设置允许排序
        self.setSortingEnabled(self.sorting)

    # ----------------------------------------------------------------------
    def registerEvent(self):
        """注册GUI更新相关的事件监听"""
        self.signal.connect(self.updateEvent)
        self.eventEngine.register(self.eventType, self.signal.emit)

    # ----------------------------------------------------------------------
    def updateEvent(self, event):
        """收到事件更新"""
        data = event.value
        self.updateData(data)

    # ----------------------------------------------------------------------
    def updateData(self, data):
        """将数据更新到表格中"""
        # 如果允许了排序功能，则插入数据前必须关闭，否则插入新的数据会变乱
        if self.sorting:
            self.setSortingEnabled(False)

        # 如果设置了dataKey，则采用存量更新模式
        if self.dataKey:
            key = data.__getattribute__(self.dataKey)
            # 如果键在数据字典中不存在，则先插入新的一行，并创建对应单元格
            if key not in self.dataDict:
                self.insertRow(0)
                d = {}
                for n, header in enumerate(self.headerList):
                    content = data.__getattribute__(header)
                    cellType = self.headerDict[header]['cellType']
                    cell = cellType(content, self.mainEngine)

                    if self.font:
                        cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

                    if self.saveData:  # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data

                    self.setItem(0, n, cell)
                    d[header] = cell
                self.dataDict[key] = d
            # 否则如果已经存在，则直接更新相关单元格
            else:
                d = self.dataDict[key]
                for header in self.headerList:
                    content = data.__getattribute__(header)
                    cell = d[header]
                    cell.setContent(content)

                    if self.saveData:  # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data
                        # 否则采用增量更新模式
        else:
            self.insertRow(0)
            for n, header in enumerate(self.headerList):
                content = data.__getattribute__(header)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content, self.mainEngine)

                if self.font:
                    cell.setFont(self.font)

                if self.saveData:
                    cell.data = data

                self.setItem(0, n, cell)

                # 调整列宽
        self.resizeColumns()

        # 重新打开排序
        if self.sorting:
            self.setSortingEnabled(True)

    # ----------------------------------------------------------------------
    def resizeColumns(self):
        """调整各列的大小"""
        self.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)

    # ----------------------------------------------------------------------
    def setSorting(self, sorting):
        """设置是否允许根据表头排序"""
        self.sorting = sorting

    # ----------------------------------------------------------------------
    def saveToCsv(self):
        """保存表格内容到CSV文件"""
        # 先隐藏右键菜单
        self.menu.close()

        # 获取想要保存的文件名
        path = QFileDialog.getSaveFileName(self, '保存数据', '', 'CSV(*.csv)')

        try:
            if not path.isEmpty():
                with open(path, 'wb') as f:
                    writer = csv.writer(f)

                    # 保存标签
                    headers = [header.encode('gbk') for header in self.headerList]
                    writer.writerow(headers)

                    # 保存每行内容
                    for row in range(self.rowCount()):
                        rowdata = []
                        for column in range(self.columnCount()):
                            item = self.item(row, column)
                            if item is not None:
                                rowdata.append(
                                    item.text().encode('gbk'))
                            else:
                                rowdata.append('')
                        writer.writerow(rowdata)
        except IOError:
            pass

    # ----------------------------------------------------------------------
    def initPopMenu(self):
        """初始化右键菜单"""
        pass
        self.menu = QMenu(self)

        # saveAction = QAction('保存内容', self)
        # saveAction.triggered.connect(self.saveToCsv)

        # self.menu.addAction(saveAction)

    # ----------------------------------------------------------------------
    def contextMenuEvent(self, event):
        """右键点击事件"""
        self.menu.popup(QCursor.pos())


########################################################################
class BasicCell(QTableWidgetItem):
    """基础的单元格"""

    # ----------------------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(BasicCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)

    # ----------------------------------------------------------------------
    def setContent(self, text):
        """设置内容"""
        # if text == '0' or text == '0.0' or text is None:
        # if text is None:
        #     self.setText('0.00')
        # else :
        self.setText(str(text))


########################################################################
class NumCell(QTableWidgetItem):
    """用来显示数字的单元格"""

    # ----------------------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(NumCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)

    # ----------------------------------------------------------------------
    def setContent(self, text):
        """设置内容"""
        # 考虑到NumCell主要用来显示OrderID和TradeID之类的整数字段，
        # 这里的数据转化方式使用int类型。但是由于部分交易接口的委托
        # 号和成交号可能不是纯数字的形式，因此补充了一个try...except
        try:
            num = int(text)
            self.setData(Qt.DisplayRole, num)
        except ValueError:
            self.setText(text)
