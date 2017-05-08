# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/5/4
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk
import math


def outputmoney(number):
    if number is None or number == '':
        return ""

    if number < 0:
        return '-' + outputdollars(math.floor(abs(number))) + outputcents(abs(number))
    else:
        return outputdollars(math.floor(number)) + outputcents(number)


# 格式化金额
def outputdollars(number):
    """
    处理小数点钱的数字
    :param number: 
    :return: 
    """
    if len(str(number)) <= 3:
        return '0' if number == '' else str(number)
    else:
        mod = len(str(number)) % 3
        output = '' if mod == 0 else str(number)[0:mod]
        for i in range(int(len(str(number)) / 3)):
            if mod == 0 and i == 0:
                output += str(number)[mod + 3 * i: mod + 3 * i + 3]
            else:
                output += ',' + str(number)[mod + 3 * i:mod + 3 * i + 3]
        return str(output)

def outputcents(amount):
    """
    处理小数点后的数字
    :param amount: 
    :return: 
    """
    a = math.floor(amount)
    amount = round((amount - a) * 100)
    return '.0' + str(amount) if amount < 10 else '.' + str(amount)


if __name__ == '__main__':
    a = 11111324424.10
    print(outputmoney(a))
    # print(outputcents(a))
    # print(outputdollars(math.floor(a)))
