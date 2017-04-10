# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/7
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk
import csv

import sys


file_path = '/Users/eranchang/Desktop/ee1.csv'
print(sys.getdefaultencoding())
with open(file_path, 'w') as f:
    writer = csv.writer(f)

    # 保存标签
    # for header in self.headerDict:
    #     print(header)
    #     writer.writerow(header.encode('gbk'))
    # headers = [header.encode('gbk') for header in self.headerList]
    # headers = ['计算日', '现金总额', '现金->资管', '现金->货基', '现金->协存', '现金->兑付投资人', '资管->现金', '货基->现金', '协存->现金', '投资人->现金', '现金收入', '提取费用']
    headers = ['计算日', '现金总额', '现金资管', '现金货基', '现金协存', '现金兑付投资人', '资管现金', '货基现金', '协存现金', '投资人现金', '现金收入', '提取费用']
    # header = [h.encode('gbk') for h in headers]
    header = [h.encode('gb2312') for h in headers]

    print(header)
    writer.writerow(header)
    # for h in headers:


