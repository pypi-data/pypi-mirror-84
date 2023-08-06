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
from tw_stock_plugin.core.update_stock import UpdateStock
from tw_stock_plugin.core.stock_trading import StockTrading

# UpdateStock.main()

date_ = datetime(2020, 11, 6).date()
stock_trading = StockTrading(date_=date_)
print(stock_trading.get_all().get('6236').change)
