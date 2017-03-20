# -*- coding: utf-8 -*-
import ctypes
import os
import platform

import sys
from pandas import json

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import MainWindow
from BasicWidget import BASIC_FONT

# 图标文件路径名
path = os.path.abspath(os.path.dirname(__file__))
ICON_FILENAME = 'zhnlk.ico'
ICON_FILENAME = os.path.join(path, ICON_FILENAME)

SETTING_FILENAME = 'FC_setting.json'
SETTING_FILENAME = os.path.join(path, SETTING_FILENAME)


def main():

    # 设置windows下的地步任务栏图标
    if 'Windows' in platform.uname():
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('feeCalculate')

    # 初始化Qt应用对象
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_FILENAME))
    app.setFont(BASIC_FONT)

    # 设置窗口皮肤
    try:
        f = open(SETTING_FILENAME)
        setting = json.load(f)
        if setting['darkStyle']:
            import qdarkStyle
            app.setStyleSheet(qdarkStyle.load_stylesheet(pyside=False))
    except:
        pass

    # 初始化主窗口
    mainWindow = MainWindow.MainWindow()
    mainWindow.showMaximized()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
