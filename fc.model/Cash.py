# -*- coding: utf-8 -*-


class Cash:
    @property
    def date(self):
        return 'date'

    def total_cash(self):
        return 'total_cash'

    def cash_to_assert_mgt(self):
        pass

    def cash_to_money_fund(self):
        pass

    def cash_to_protocol_deposit(self):
        pass

    @setattr()
    def cash_to_investor(self):
        pass

    def assert_mgt_to_cash(self):
        pass

    def money_fund_to_cash(self):
        pass

    def protocol_deposit_to_cash(self):
        pass

    def investor_to_cash(self):
        pass

if __name__ == '__main__':
    c = Cash()
