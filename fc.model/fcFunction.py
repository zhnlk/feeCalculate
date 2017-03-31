# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
import json
import os

from fcConstant import DB_FILENAME, SETTING_FILENAME


def loadSqliteSetting():
    """载入Sqlite3数据库的配置"""

    # setting = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, SETTING_FILENAME))

    try:
        # f = open(setting)
        # setting = json.load(f)
        # logging = setting['DBlogging']
        # SQLALCHEMY_DATABASE_URI
        uri = "sqlite:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, DB_FILENAME))
    except:
        uri = "sqlite:///:memory:"
        logging = False

    return uri


if __name__ == '__main__':
    uri = loadSqliteSetting()
    print(uri)
