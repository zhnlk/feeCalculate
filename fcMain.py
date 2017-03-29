# -*- coding: utf-8 -*-
import ctypes
import json
import os
import platform

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from BasicWidget import BASIC_FONT

from MainEngine import MainEngine
from MainWindow import MainWindow
from fcConstant import ICON_FILENAME
from fcConstant import SETTING_FILENAME

# 设置路径
path = os.path.abspath(os.path.dirname(__file__))
ICON_FILENAME = os.path.join(path, ICON_FILENAME)
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
    except:
        pass

    # 初始化主窗口
    mainEngine = MainEngine()
    mainWindow = MainWindow(mainEngine, mainEngine.eventEngine)
    mainWindow.showMaximized()
    sys.exit(app.exec_())

def tpath():
    print(ICON_FILENAME)
    try:
        f = open(SETTING_FILENAME)
        setting = json.load(f)
        print(setting)
        print(setting['darkStyle'])
    except:
        pass



if __name__ == '__main__':
    main()
    # tpath()