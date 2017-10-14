# -*- coding: utf-8 -*-
import em_scrapy
from em_scrapy import EMMFScrapy
import basics
import scrapy
from basics import *
from k import KAs
import sys
from dd_scrapy import EMDDScrapy


basics.init()

if sys.argv[1] == 'mf':
    logger.info("start...")
    #refresh money flow
    money_flow = EMMFScrapy("http://data.eastmoney.com/zjlx/detail.html", 'dataurl.*token=(\d|\w+)\{', \
    "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=5000&js=var%20sRcSWRth={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=<TOKEN>&cmd=C._AB&sty=DCFFITA&rt=50213657")
    money_flow.do()

#refresh k data
if sys.argv[1] == 'rk':
    kl = basics.get_k_list()
    basics.refresh_k_data(kl, k='yes')

    basics.refresh_k_data(kl, k="yes", k_type = '5')
    print("5 finished")

    basics.refresh_k_data(kl, k="yes", k_type = '15')
    print("15 finished")

    basics.refresh_k_data(kl, k="yes", k_type = '30')
    print("30 finished")

    basics.refresh_k_data(kl, k="yes", k_type = '60')
    print("60 finished")

    basics.refresh_k_data(kl, k="yes", k_type = 'W')
    print("W finished")

    basics.refresh_k_data(kl, k="yes", k_type = 'M')
    print("M finished")

#######refresh classified
if sys.argv[1] == 'rc':
    basics.refresh_classified()

if sys.argv[1] == 'rdd_all':
    logger.info('rdd_all')
    dd = EMDDScrapy()
    cl = basics.get_k_list()
    for code in cl:
        dd.refresh_st_dd(code, number = 500)

if sys.argv[1] == 'rdd_today':
    logger.info('rdd_today')
    dd = EMDDScrapy()
    dd.refresh_latest_dd(number = 500)

if sys.argv[1] == 'need change':
    #######Anal
    dk = KAs(['600602'], start_time = '2016-04-07', end_time = '2016-12-1')
    dk.get_k_data()

    #print dk.data[dk.codes[0]]

    r = dk.rchange_k_auto(dk.data[dk.codes[0]], delay = 3, average = 8, ignore_max_day = 20, ignore = 0.05, cut_point = 0.05)
    print "##########RESULT#############3"
    print r


