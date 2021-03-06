# encoding: UTF-8
import datetime

from controller.EventEngine import *
from services import AssetService, CashService, CommonService, AgreementService, FundService
from utils import StaticValue as SV

class MainEngine(object):
    """主引擎"""

    def __init__(self):
        """Constructor"""
        # 记录今日日期
        self.todayDate = datetime.date.today()

        # 创建事件引擎
        self.eventEngine = EventEngine()
        self.eventEngine.start()

    def exit(self):
        """退出程序前调用，保证正常退出"""
        # 停止事件引擎
        self.eventEngine.stop()

    def getMainCostData(self):
        today_asset_cost = CommonService.get_total_evaluate_detail(1)[0]['cost']
        return self.todayDate, today_asset_cost

    def getMainFeeData(self):
        rate, duration = self.getFeeConstrant()
        return rate, duration

        # def getMainTotalValuationData(self):
        # return Valuation.listAll()

    def getFeeConstrant(self):
        rate = ['0.02%', '0.30%', '0.04%']
        duration = ['360', '360', '365']
        return rate, duration

    def getTodayFee(self, date):
        # v = Valuation.findByDate(date)
        # if v is None:
        return '0', '0', '0', '0'
        # else:
        # return v.fee_1, v.fee_2, v.fee_3, v.fee_4

    def add_agreement_class(self, name='', rate=0.03, threshold_amount=0, threshold_rate=0):
        """
        增加协存类别
        :param name: 
        :param rate: 
        :param threshold_amount: 
        :param threshold_rate: 
        :return: 
        """
        AssetService.add_agreement_class(name, rate, threshold_amount, threshold_rate)

    def add_fund_class(self, name):
        """
        增加基金类别
        :param name: 
        :return: 
        """
        AssetService.add_fund_class(name=name)

    def add_management_class(self, name, trade_amount, ret_rate, rate_days, start_date, end_date,
                             bank_fee_rate, bank_days, manage_fee_rate, manage_days, cal_date=datetime.date.today()):
        """
        增加资管类别
        :param name: 
        :param trade_amount: 
        :param ret_rate: 
        :param rate_days: 
        :param start_date: 
        :param end_date: 
        :param bank_fee_rate: 
        :param bank_days: 
        :param manage_fee_rate: 
        :param manage_days: 
        :param cal_date: 
        :return: 
        """
        AssetService.add_management_class(name, trade_amount, ret_rate, rate_days, start_date, end_date,
                                          bank_fee_rate, bank_days, manage_fee_rate, manage_days, cal_date)

    def get_all_asset_ids_by_type(self, asset_type):
        """
        根据资产类型获取对应的uuid与asset_name
        :param asset_type: 资产类型
        :return: 
        """
        return CommonService.get_all_asset_ids_by_type(asset_type)

    def get_cash_detail_by_days(self, days=0):
        """
        获取现金明细
        :param days:获取days内的现金明细
        :return 现金明细的dict
        """
        return CashService.get_cash_detail_by_days(days)

    def get_cash_detail_by_period(self, start=datetime.date.today(), end=datetime.date.today()):
        """
        筛选现金明细
        :param start: 
        :param end: 
        :return: 
        """
        return CashService.get_cash_detail_by_period(start=start, end=end)

    def add_cash_daily_data(self, cal_date, draw_amount, draw_fee, deposit_amount, ret_amount):
        """
        增加现金明细记录
        :param draw_amount: 兑付
        :param draw_fee: 提取费用
        :param deposit_amount: 流入
        :param ret_amount:现金收入
        :return None 
        """
        CashService.add_cash_daily_data(cal_date, draw_amount, draw_fee, deposit_amount, ret_amount)

    def add_agreement_daily_data(self, cal_date, asset_id, ret_carry_asset_amount, purchase_amount,
                                 redeem_amount):
        """
        添加协存每日记录
        :param asset_id: 
        :param ret_carry_asset_amount: 
        :param purchase_amount: 
        :param redeem_amount: 
        :return: 
        """
        AssetService.add_agreement_daily_data(cal_date, asset_id, ret_carry_asset_amount, purchase_amount,
                                              redeem_amount)

    def add_fund_daily_data(self, cal_date, asset_id, ret_carry_cash_amount, purchase_amount, redeem_amount,
                            ret_amount):
        '''
        添加货基每日记录
        :param asset_id:计算日期
        :param ret_carry_cash_amount:收益结转现金
        :param purchase_amount:申购金额
        :param redeem_amount:赎回金额
        :param ret_amount:收益
        :return:None
        '''
        AssetService.add_fund_daily_data(cal_date, asset_id, ret_carry_cash_amount, purchase_amount, redeem_amount,
                                         ret_amount)

    def get_agreement_detail_by_days(self, days=0):
        """
        获取协存明细记录
        :param days: 
        :return: 
        """
        return AssetService.get_agreement_detail_by_days(days)

    def get_single_agreement_detail_by_period(self, asset_id=None, start=datetime.date.today(),
                                              end=datetime.date.today()):
        """
        获取过滤后的协存明细记录
        :param asset_id: 
        :param start: 
        :param end: 
        :return: 
        """
        return AssetService.get_single_agreement_detail_by_period(asset_id=asset_id, start=start, end=end)

    def get_fund_detail_by_days(self, days=0):
        """
        获取货基明细记录
        :param days: 
        :return: 
        """
        return AssetService.get_fund_detail_by_days(days)

    def get_single_fund_detail_by_period(self, asset_id=None, start=datetime.date.today(), end=datetime.date.today()):
        """
        获取过滤后的货基明细f
        :param asset_id: 
        :param start: 
        :param end: 
        :return: 
        """
        return AssetService.get_single_fund_detail_by_period(asset_id=asset_id, start=start, end=end)

    def get_total_fund_statistic(self):
        """
        获取当天货基汇总
        :return: 
        """
        return AssetService.get_total_fund_statistic()

    def get_total_management_statistic(self):
        """
        资管汇总表
        :return: 
        """
        # return AssetService.get_total_management_statistic()
        return AssetService.get_total_management_statistic_by_days(7)

    def get_total_management_statistic_period(self, start_date, end_date):
        """
        筛选后的资管汇总表
        :param start_date: 
        :param end_date: 
        :return: 
        """
        return AssetService.get_total_management_statistic_period(start_date, end_date)

    def get_all_management_detail(self):
        """
        资管相关明细
        :return: 
        """
        return AssetService.get_all_management_detail()

    def get_total_evaluate_detail(self, days=0):
        """
        估计明细
        :param days: 
        :return: 
        """
        return CommonService.get_total_evaluate_detail(days)

    def get_total_evaluate_detail_by_period(self, start=datetime.date.today(), end=datetime.date.today()):
        """
        估值明细筛选
        :param start: 
        :param end: 
        :return: 
        """
        return CommonService.get_total_evaluate_detail_by_period(start=start, end=end)

    def get_today_fees(self):
        """
        获取今日费用
        :return: 
        """
        return CommonService.get_today_fees()

    def get_management_fee_by_id(self, uuid):
        """
        获取费用明细
        :param uuid: 
        :return: 
        """
        return AssetService.get_management_fee_by_id(cal_date=datetime.date.today(), asset_id=uuid)

    def get_management_adjust_fee_by_id(self, uuid):
        """
        获取费用调整明细
        :param uuid: 
        :return: 
        """
        result = list()
        allFees = AssetService.get_management_fee_by_id(cal_date=datetime.date.today(), asset_id=uuid)
        for f in allFees:
            if f['fee_type'] in [2, 3]:
                result.append(f)
        return result

    def add_asset_fee_with_asset_and_type(self, amount=0, cal_date=datetime.date.today()):
        """
        增加今日资金成本
        :param amount: 
        :param cal_date: 
        :return: 
        """
        CommonService.add_daily_fee(cal_date, amount)

    def get_total_agreement_statistic_by_days(self, days=0):
        """
        协存存量表
        :param days: 
        :return: 
        """
        return AgreementService.get_total_agreement_statistic_by_days(days=days)

    def get_total_agreement_statistic_by_period(self, start=datetime.date.today(), end=datetime.date.today()):
        """
        协存存量表
        :param start: 
        :param end: 
        :return: 
        """
        return AgreementService.get_total_agreement_statistic_by_period(start_date=start, end_date=end)

    def get_total_fund_statistic_by_days(self, days=0):
        """
        货基存量表
        :param days: 
        :return: 
        """
        return FundService.get_total_fund_statistic_by_days(days=days)

    def get_total_fund_statistic_by_period(self, start=datetime.date.today(), end=datetime.date.today()):
        """
        货基存量表
        :param start: 
        :param end: 
        :return: 
        """
        return FundService.get_total_fund_statistic_by_period(start_date=start, end_date=end)

    def clean_data_by_date(self, cal_date=datetime.date.today()):
        """
        清除本日数据
        :param cal_date: 
        :return: 
        """
        CommonService.clean_data_by_date(cal_date=cal_date)

    def get_cash_input_detail_by_date_dic(self, cal_date=datetime.date.today()):
        """
        修改时获取现金的明细
        :param cal_date: 
        :return: 
        """
        return CashService.get_cash_input_detail_by_date_dic(cal_date)

    def update_cash_input_by_id_type(self, cash_id, amount, cash_type, cal_date):
        """
        对现金进行修改
        :param cash_id: 
        :param amount: 
        :param cash_type: 
        :param cal_date: 
        :return: 
        """
        CashService.update_cash_input_by_id_type(cash_id, amount, cash_type, cal_date)

    def get_agreement_input_detail_by_id_date_dic(self, agreement_id=None, cal_date=datetime.date.today()):
        """
        修改时获取协存的明细
        :param agreement_id: 
        :param cal_date: 
        :return: 
        """
        return AgreementService.get_agreement_input_detail_by_id_date_dic(agreement_id=agreement_id,
                                                                          cal_date=cal_date)

    def update_agreement_input_by_id_type(self, agreement_id=None, amount=0, agreement_type=SV.ASSET_TYPE_RET_CARRY,
                                          cal_date=datetime.date.today()):
        """
        对协存进行修改
        :param agreement_id: 
        :param amount: 
        :param agreement_type: 
        :param cal_date: 
        :return: 
        """
        AgreementService.update_agreement_input_by_id_type(agreement_id=agreement_id, amount=amount,
                                                           agreement_type=agreement_type, cal_date=cal_date)

    def get_fund_input_by_id_date_dic(self, fund_id=None, cal_date=datetime.date.today()):
        """
        修改时获取货基的明细
        :param cal_date: 
        :return: 
        """
        return FundService.get_fund_input_by_id_date_dic(fund_id=fund_id,
                                                         cal_date=cal_date)

    def update_fund_input_by_id_date(self, fund_trade_id=None, cal_date=datetime.date.today(), amount=0, is_asset=True):
        """
        对货基进行修改
        :param cal_date: 
        :param amount: 
        :param is_asset: 
        :return: 
        """
        FundService.update_fund_input_by_id_date(fund_trade_id=fund_trade_id,
                                                 cal_date=cal_date,
                                                 amount=amount,
                                                 is_asset=is_asset)

    def clean_management_record_by_id(self, uuid=None):
        """
        删除资管明细
        :param uuid: 
        :return: 
        """
        CommonService.clean_management_record_by_id(management_id=uuid)
