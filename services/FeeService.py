# # encoding:utf8
#
# from __future__ import unicode_literals
#
# from datetime import date
#
# from sqlalchemy import func
#
# from models.CommonModel import session_deco
# from models.DailyFeeModel import DailyFee
# from services.CommonService import save, query
# from utils import StaticValue as SV
#
#
# @session_deco
# def get_daily_fee_last_total_amount_by_date(cal_date=date.today(), **kwargs):
#     session = kwargs.get(SV.SESSION_KEY, None)
#     ret = session.query(DailyFee, func.max(DailyFee.time).label('max_time')).filter(
#         DailyFee.is_active,
#         DailyFee.date == cal_date
#     ).one()
#
#     return ret.DailyFee.total_amount if ret.DailyFee else 0.0
#
#
# def add_fee_with_date(cal_date=date.today(), amount=0.0):
#     save(
#         DailyFee(
#             cal_date=cal_date,
#             amount=get_daily_fee_last_total_amount_by_date(cal_date=cal_date) + amount
#         )
#     )
#
#
# def get_daily_fee(cal_date=date.today()):
#     fees = query(DailyFee).filter(DailyFee.date == cal_date)
#     if fees.count() > 0:
#         return fees[-1].amount
#     else:
#         return 0.0
#
#
# if __name__ == '__main__':
#     # print(get_daily_fee_last_total_amount_by_date(cal_date=date.today()))
#     add_fee_with_date(cal_date=date.today(), amount=1000)
