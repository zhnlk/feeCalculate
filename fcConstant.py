# encoding: UTF-8

# 默认空值
import os

import sys

EMPTY_STRING = ''
EMPTY_UNICODE = ''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

# 程序相关设置
ICON_FILENAME = 'zhnlk.ico'
DB_FILENAME = 'data-test.db'


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


path = os.path.dirname(__file__)
print('path:..' + path)
ICON_FILENAME = resource_path(os.path.join(path, ICON_FILENAME))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + resource_path(os.path.join(path, 'data-test.db'))


def disp():
    print('path:...' + path)
    print('ICON_FILENAME:...' + ICON_FILENAME)
    print('SQLALCHEMY_DATABASE_URI:...' + SQLALCHEMY_DATABASE_URI)


if __name__ == '__main__':
    disp()
