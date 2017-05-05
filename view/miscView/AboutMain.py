# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout


class AboutWidget(QDialog):
    """显示关于信息"""

    def __init__(self, parent=None):
        """Constructor"""
        super(AboutWidget, self).__init__(parent)

        self.initUi()

    def initUi(self):
        """"""
        self.setWindowTitle('About Fee Calculate')

        text = """
                Developed by zhnlk && wzjwhtur

                Version: 0.0.1

                License：MIT

                Mail：zhangyanan@ktjr.com && wangzhijie@ktjr.com

                Github：github.com/zhnlk && github.com/wzjwhtur

                """

        label = QLabel()
        label.setText(text)
        label.setMinimumWidth(500)

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)