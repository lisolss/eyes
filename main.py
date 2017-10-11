# -*- coding: utf-8 -*-
import em_scrapy
from em_scrapy import EMMFScrapy
import basics
import scrapy
from basics import *

basics.init()
logger.info("start...")
#refresh money flow
money_flow = EMMFScrapy("http://data.eastmoney.com/zjlx/detail.html", 'dataurl.*token=(\d|\w+)\{', \
"http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=5000&js=var%20sRcSWRth={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=<TOKEN>&cmd=C._AB&sty=DCFFITA&rt=50213657")
money_flow.do()

#refresh k data
"""
basics.refresh_k_data(basics.get_k_list(), k="yes", k_type = '5')
print("5 finished")
basics.refresh_k_data(basics.get_k_list(), k="yes", k_type = '15')
print("15 finished")

basics.refresh_k_data(basics.get_k_list(), k="yes", k_type = '30')
print("30 finished")

basics.refresh_k_data(basics.get_k_list(), k="yes", k_type = '60')
print("60 finished")

basics.refresh_k_data(basics.get_k_list(), k="yes", k_type = 'W')
print("W finished")

basics.refresh_k_data(basics.get_k_list(), k="yes", k_type = 'M')
print("M finished")
"""
