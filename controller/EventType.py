# encoding: UTF-8

'''
本文件仅用于存放对于事件类型常量的定义。

由于python中不存在真正的常量概念，因此选择使用全大写的变量名来代替常量。
这里设计的命名规则以EVENT_前缀开头。

常量的内容通常选择一个能够代表真实意义的字符串（便于理解）。

建议将所有的常量定义放在该文件中，便于检查是否存在重复的现象。
'''

# 系统相关
EVENT_TIMER = 'eTimer'  # 计时器事件，每隔1秒发送一次
EVENT_LOG = 'eLog'  # 日志事件，全局通用

# 主界面相关
EVENT_MAIN_COST = 'eMainCost'  # 主界面成本框
EVENT_MAIN_FEE = 'eMainFee'  # 主界面费用框
EVENT_MAIN_ASSERT_DETAIL = 'eMainAssertDetail'  # 主界面存量资产详情
EVENT_MAIN_VALUATION = 'eMainValuation'  # 主界面总估值表

# 分界面
EVENT_CASH = 'eCash'  # 现金的相关事件
EVENT_PD = 'ePd'  # 协存的相关事件
EVENT_PD_INPUT = 'ePdInput'  # 协存输入的下拉框事件
EVENT_MF = 'eMf'  # 货基的相关事件
EVENT_MF_INPUT = 'eMfInput'  # 货基输入的下拉框事件
EVENT_AM = 'eAm'  # 存管的相关事件
EVENT_AM_INPUT = 'eAmInput'  # 存管相关事件

# 调整界面
EVENT_ADJUST_VIEW = 'eAdjustView'  # 调整记录查看
EVENT_ADJUST_INPUT = 'eAdjustInput'  # 调整记录输入

EVENT_ERROR = 'eError.'  # 错误回报事件


def test():
    """检查是否存在内容重复的常量定义"""
    check_dict = {}

    global_dict = globals()

    for key, value in global_dict.items():
        if '__' not in key:  # 不检查python内置对象
            if value in check_dict:
                check_dict[value].append(key)
            else:
                check_dict[value] = [key]

    for key, value in check_dict.items():
        if len(value) > 1:
            print(u'存在重复的常量定义:' + str(key))
            for name in value:
                print(name)
            print('')

    print('测试完毕')


# 直接运行脚本可以进行测试
if __name__ == '__main__':
    test()
