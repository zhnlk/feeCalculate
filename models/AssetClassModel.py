# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import Integer

from models.CommonModel import *

__all__ = ['AssetClass']


class AssetClass(MixinBase):
    name = Column(String(50), default='')
    type = Column(Integer, default=1)

    def __init__(self, name='', type=1):
        MixinBase.__init__(self)
        self.name = name
        self.type = type

    def __repr__(self):
        return '<AssetClass id=%s, name=%s, type=%s>' % (self.id, self.name, self.type)
