# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/7
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk

import xlsxwriter

file_path = '/Users/eranchang/Desktop/'

workbook = xlsxwriter.Workbook(file_path + 'hello.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Hello world')

workbook.close()
