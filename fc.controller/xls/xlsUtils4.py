# -*- coding: utf-8 -*-
#coding=utf-8
#######################################################
#filename:test_pyExcelerator.py
#author:defias
#date:xxxx-xx-xx
#function：新建excel文件并写入数据
#######################################################
import pyExcelerator
#创建workbook和sheet对象
wb = pyExcelerator.Workbook()
ws = wb.add_sheet(u'第一页')
#设置样式
myfont = pyExcelerator.Font()
myfont.name = u'Times New Roman'
myfont.bold = True
mystyle = pyExcelerator.XFStyle()
mystyle.font = myfont
#写入数据，使用样式
ws.write(0,0,u'ni hao 帕索！',mystyle)
#保存该excel文件,有同名文件时直接覆盖
wb.save('E:\\Code\\Python\\mini.xls')
print('创建excel文件完成！')