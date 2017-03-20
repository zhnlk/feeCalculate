# -*- coding: utf-8 -*-
#coding=utf-8
#######################################################
#filename:test_pyExcelerator_read.py
#author:defias
#date:xxxx-xx-xx
#function：读excel文件中的数据
#######################################################
import pyExcelerator
#parse_xls返回一个列表，每项都是一个sheet页的数据。
#每项是一个二元组(表名,单元格数据)。其中单元格数据为一个字典，键值就是单元格的索引(i,j)。如果某个单元格无数据，那么就不存在这个值
sheets = pyExcelerator.parse_xls('E:\\Code\\Python\\testdata.xls')
print(sheets)