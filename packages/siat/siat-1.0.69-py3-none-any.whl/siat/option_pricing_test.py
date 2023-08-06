# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:08:44 2020

@author: Peter
"""


import os; os.chdir("S:/siat")
from siat.option_pricing import *


import time
tupTime = time.localtime(1604350755)#秒时间戳
stadardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
print(stadardTime)


ticker="AAPL"
mdate="2020-11-06"
opt_call, opt_put=option_chain(ticker,mdate,printout=False)


from siat.stock import *
div=stock_dividend('AAPL','2020-1-1','2020-11-3')
splt=stock_split('AAPL','2020-1-1','2020-11-3')


df=predict_stock_price_by_option('AAPL',lastndays=7,power=4)

df=predict_stock_price_by_option('02020.HK',lastndays=7,power=4)
df=predict_stock_price_by_option('2331.HK',lastndays=7,power=4)
df=predict_stock_price_by_option('1368.HK',lastndays=7,power=4)

splt=stock_split('NKE','2020-1-1','2020-11-3')
df=predict_stock_price_by_option('NKE',lastndays=30,power=5)

splt=stock_split('ADS.DE','2020-1-1','2020-11-3')
df=predict_stock_price_by_option('ADS.DE',lastndays=30,power=5)

splt=stock_split('JD','2020-1-1','2020-11-3')
df=predict_stock_price_by_option('JD',lastndays=30,power=6)

splt=stock_split('BABA','2020-1-1','2020-11-3')
df=predict_stock_price_by_option('BABA',lastndays=30,power=6)
