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
from tw_stock_plugin.core.stock_margin_trading import StockMarginTrading

date_ = datetime(2020, 10, 30).date()
# init stock margin trading object with specific date
stock_margin_trading = StockMarginTrading(date_=date_)
# getting all margin trading data in 2020/10/30
margin_trading_all = stock_margin_trading.get_all()
# getting 2330 margin trading data in 2020/10/30
margin_trading_1101 = margin_trading_all['1101']
# print 2330 margin purchase
print(margin_trading_1101.note)
# print 2330 short covering
