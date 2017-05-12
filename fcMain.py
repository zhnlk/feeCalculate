# -*- coding: utf-8 -*-

import ctypes
import platform
import sys
from datetime import date

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from controller.MainEngine import MainEngine
from services.AssetService import cal_all_agreement_ret, cal_all_management_ret_and_fee
from utils.StaticValue import ICON_FILENAME
from view.BasicWidget import BASIC_FONT
from view.MainWindow import MainWindow


def main():
    # 设置windows下的地步任务栏图标
    if 'Windows' in platform.uname():
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('feeCalculate')

    # 初始化Qt应用对象
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_FILENAME))
    app.setFont(BASIC_FONT)

    # 初始化主窗口
    mainEngine = MainEngine()
    mainWindow = MainWindow(mainEngine, mainEngine.eventEngine)
    mainWindow.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    cal_all_agreement_ret(cal_date=date.today())
    cal_all_management_ret_and_fee(cal_date=date.today())
    main()
