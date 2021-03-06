# -*- coding: utf-8 -*-
import em_scrapy
from em_scrapy import EMMFScrapy
import basics
import scrapy
from basics import *
import daily_vol
from k import KAs
import sys
from ticks import TKAs
from dd_scrapy import EMDDScrapy
import tradeday

if sys.argv[1] == 'mf':
    basics.init()
    logger.info("start...")
    #refresh money flow
    money_flow = EMMFScrapy("http://data.eastmoney.com/zjlx/detail.html", 'dataurl.*token=(\d|\w+)\{', \
    "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=5000&js=var%20sRcSWRth={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=<TOKEN>&cmd=C._AB&sty=DCFFITA&rt=50213657")
    money_flow.do()

#refresh k data
if sys.argv[1] == 'rk':

    basics.init(log_file = sys.path[0] + '/test_rk.log')

    kl = basics.get_k_list()
    #kl = basics.get_k_list_tdx()
    #time.sleep(99)
    basics.refresh_k_data(kl, True)

if sys.argv[1] == 'rkf':
    basics.init()
    kl = basics.get_k_list()
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
    basics.init()
    basics.refresh_classified_tdx()


if sys.argv[1] == 'rdd_all':
    basics.init()
    logger.info('rdd_all')
    dd = EMDDScrapy()
    cl = basics.get_k_list()
    for code in cl:
        dd.refresh_st_dd(code, number = 500)

if sys.argv[1] == 'rdd_today':
    basics.init()
    logger.info('rdd_today')
    dd = EMDDScrapy()
    dd.refresh_latest_dd(number = 500)

if sys.argv[1] == 'rttoday':
    basics.init(log_file = sys.path[0] + '/test_rt.log')
    logger.info('refresh ticks')
    
    l = datetime.datetime.now()

    cvs_lastest = l.strftime("%Y%m%d")
    if tradeday.is_tradeday(cvs_lastest) == 1:
        dd = TKAs()
        dd.refresh_all_ticks(cvs_lastest)
    
    del dd
    exit(0)
    

if sys.argv[1] == 'rt':
    basics.init(log_file = sys.path[0] + '/test_rt.log')

    #l = datetime.datetime.now()
    l = datetime.datetime.strptime("2019-01-27", "%Y-%m-%d")
    dd = TKAs()
    for i in range(5):
        #today = l.weekday()
        #if today >= 5:
        #    l = l - datetime.timedelta(days=1)
        #    continue
        
        cvs_lastest = l.strftime("%Y%m%d")
        if tradeday.is_tradeday(cvs_lastest) == 1:
            print cvs_lastest
            dd.refresh_all_ticks(cvs_lastest)
        l = l - datetime.timedelta(days=1)

    del dd
    exit(0)

if sys.argv[1] == 'test':
    basics.init()
    #l = datetime.datetime.now()
    #basics.refresh_classified_tdx()
    


if sys.argv[1] == 'test_old':
    basics.init()
    #l = datetime.datetime.now()
    l = datetime.datetime.strptime("2017-11-22", "%Y-%m-%d")
    dd = TKAs()
    dd.summary_ticks('600600', l)

    del dd


import time
def back_test(dk, kl, start_time, end_time, delay = 1, average = 6, ignore_max_day = 6, ignore = 0.05, cut_point = 0.15):
    a = 0
    b = 0
    c = 0
    d = 0

    for i in range(1,100):
        
        k = random.randint(1,3591)
        code = kl[k]
        dk.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        dk.end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        
        
        if type(dk.data[code]) == type(False):
            print code
            print start_time
            print end_time
            continue
        r = dk.rchange_k_auto(dk.data[code], delay = 1, average = 6, ignore_max_day = 6, ignore = 0.05, cut_point = 0.15)

        if r == None:
            continue

        #print r['close_rate']
        if r['close_rate'] > 0:
            a = a+1
            c = c + (10000*r['close_rate'])
        else:
            b = b+1
            d = d + (10000*r['close_rate'])
    """print ("a is %d" % (a))
    print ("b is %d" % b)
    print ("c is %d" % (c))
    print ("d is %d" % d)
    print ("e is %d" % (c+d))"""
    f = {'payoff':a, 'loss':b, 'payvol':c, 'loss_vol':d, 'gap':(c+d)}
    print f
    return f
    #exit()

if sys.argv[1] == 'summary_ticks':
    basics.init()
    dd = TKAs()
    dd.summary_all()
    del dd
    exit(0)
 
if sys.argv[1] == 'summary_class':
    basics.init()
    dd = TKAs()
    dd.summary_classified_all()
    del dd
    exit(0)

if sys.argv[1] == 'sortself':

    today = datetime.datetime.strptime("2019-01-25", "%Y-%m-%d")
    fromday = 3
    ticks_top = 0.2
    ticks_sort_type = 'rate'
    ticks_sort_date = '2019-01-25'
    class_list = "all"
    ignore_value = 15000
    time_step = 30

    sort_type = ''
    

    ##################################
    if ticks_sort_date == 'today':
        ticks_sort_date = datetime.datetime.now()
        ticks_sort_date = ticks_sort_date.strftime("%Y-%m-%d")
    fromday = today - datetime.timedelta(days=(fromday-1))
    
    code_list = daily_vol.get_code_from_class(class_list, ticks_top, ticks_sort_type, ticks_sort_date)

    sort_data = {}
    dd = TKAs()
    print "xxxxxxxxxxxxxxxx111"
    for class_name, codes in code_list.items():
        print "xxxxxxxxxxxxxxxx2"
        print class_name
        print len(codes)
        sort_data[class_name] = dd.get_ticks_summary_timezone(codes, fromday, today, ignore_value, time_step)
        #print sort_data[class_name] 
        
    for name, dd in sort_data.items():

        print name
        print dd    
    print "xxxxxxxxxxxxxxxxxxxxxxxxxppppppppppppppppppppppppppppp"
    time.sleep(9999)
    
    #################################
    
    """
    sort_data.

    for class_name in sort_data:
        sort_data['class_name'][ticks_sort_type] = 
    """


    


import random
if sys.argv[1] == 'tsystem_check':
    a1=(2016,1,1,0,0,0,0,0,0)
    a2=(2017,8,1,23,59,59,0,0,0)
    df_ret = pd.DataFrame([],columns=["parameter", 'payoff', 'loss', 'payvol', 'loss_vol', 'gap'])
    start=time.mktime(a1)    #生成开始时间戳
    end=time.mktime(a2)      #生成结束时间戳
    
    kl = basics.get_k_list()
    print kl.values
    
    dk = KAs(kl.values, start_time = '2016-01-01', end_time = '2017-08-01', inmemory = True)
    dk.get_k_data()

    range_delay = range(1,2)
    range_average = range(4,5)
    range_ignore_day = range(2,4)
    range_igonre = range(4, 5)
    range_cut_point = range(5, 7)
    totall_count = len(range_delay) * len(range_average) * len(range_ignore_day) * len(range_igonre) * len(range_cut_point)
    print("The total count is %d, will take about %d minuets" % (totall_count, totall_count * 5))
    time.sleep(30)
    for i in range_delay:
        delay = i
        for i1 in range_average:
            average = i1
            for i2 in range_ignore_day:
                ignore_max_day = i2
                for i3 in map(lambda x:x/100.0, range_igonre):
                    ignore = i3
                    for i4 in map(lambda x:x/100.0, range_cut_point):
                        cut_point = i4
                        rp = "delay:%s, average:%s, ignore_max_day:%d, ignore:%f, cut_point:%f" % (delay, average, ignore_max_day, ignore, cut_point)
                        rdf = pd.DataFrame([], columns = ['payoff', 'loss', 'payvol', 'loss_vol', 'gap'])
                        for i5 in range(1,100):
                            date_touple=time.localtime(random.randint(start,end))
                            date=time.strftime("%Y-%m-%d",date_touple)
                            start_date = datetime.datetime.strptime(date,"%Y-%m-%d")
                        
                            end_date = start_date + datetime.timedelta(days=100)
                        
                            r = test(dk, kl, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), delay=delay, average = average, ignore_max_day = ignore_max_day, ignore = ignore, cut_point = cut_point)
                            rdf = rdf.append(r, ignore_index=True)
                        
                        #print rdf
                        df_ret = df_ret.append({'parameter':rp, 'payoff':rdf.payoff.mean(),'loss':rdf.loss.mean(), 'payvol':rdf.payvol.mean(),\
                            'loss_vol':rdf.loss_vol.mean(), 'gap':rdf.gap.mean()}, ignore_index=True)
                        print df_ret
                        df_ret.to_csv('./parameter.csv')
    df_ret.to_csv('./parameter.csv')
    exit()
    dk = KAs(['601992'], start_time = '2017-04-09', end_time = '2017-09-01')
    dk.get_k_data()

    #print dk.data[dk.codes[0]]
    #r = dk.rchange_k(dk.data[dk.codes[0]], starttime = dk.start_time, endtime = dk.end_time)
    #r = dk.rchange_k_auto(dk.data[dk.codes[0]], delay = 1, average = 3, ignore_max_day = 5, ignore = 0.01, cut_point = 0.05)
    r['code'] = dk.codes[0]
    print "##########RESULT#############3"
    for key,value in r.items():
        print "%s = %s" % (key, value)
    a = pd.DataFrame([r])
    print a

exit(0)
