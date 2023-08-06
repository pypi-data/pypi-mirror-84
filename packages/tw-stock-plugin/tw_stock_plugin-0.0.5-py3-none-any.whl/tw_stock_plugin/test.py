# -*- coding: utf-8 -*
"""
      ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
      ┗┳        ┗━┓
       ┃          ┣┓
       ┃          ┏┛
       ┗┓┓┏━━━━┳┓┏┛
        ┃┫┫    ┃┫┫
        ┗┻┛    ┗┻┛
    God Bless,Never Bug
"""
from datetime import datetime
from tw_stock_plugin.core.stock_info import StockInfo
from tw_stock_plugin.core.update_stock import UpdateStock
from tw_stock_plugin.core.stock_trading import StockTrading
from tw_stock_plugin.core.stock_margin_trading import StockMarginTrading
from tw_stock_plugin.core.stock_institutional_investors import StockInstitutionalInvestors

# UpdateStock.main()

date_ = datetime(2020, 11, 6).date()
# stock_info = StockInfo()
# print(stock_info.get('02001L'))
# stock_trading = StockTrading(date_=date_)
# print(stock_trading.get_all())
# print(stock_trading.get_history(code='02001L')[date_].__dict__)
# print(stock_trading.get_history(code='8921')[date_].__dict__)
# stock_institutional_investors = StockInstitutionalInvestors(date_=date_)
# print(stock_institutional_investors.get_all())
stock_margin_trading = StockMarginTrading(date_=date_)
n = stock_margin_trading.get_all()['4737'].note
print(n)
print(len(n))
print(len(n.strip()))
