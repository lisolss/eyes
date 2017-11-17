# -*- coding: utf-8 -*-
import em_scrapy
from em_scrapy import EMMFScrapy
import basics
import scrapy
from basics import *
from k import KAs
import sys
from dd_scrapy import EMDDScrapy
from itertools import product
#print list(product([1,2,3,4], [5, 6], [7,8], [9]))

#pa is 2d array
#basics.init()
"""
   average    buy    buy_date  close_date  close_rate  close_value    code  \
0   6.8608  6.768  2017-04-10  2017-09-01    0.031324         6.98  601992

        dep    dep_date  dep_day  last_day       top    top_date  top_day
0 -0.156324  2017-07-17       99       145  0.331413  2017-04-17        8
"""

"""
return:
0: 没啥变化
1: 下跌状态
2: 上涨状态
"""
gi = 0
def k_form(dk, ignore = 0.1):
    r = dk.rchange_k(dk.codes[0])

    average_gap = r['average']/r['close']
    average_gap_v = 1 - average_gap if average_gap <= 1 else average_gap - 1
    
    if average_gap_v < ignore: 
        r['form'] = 0
        return r
    r['form'] = 1
    return r
basics.init()

def vol_Test():
    cl = basics.get_k_list()
    
    df = pd.DataFrame()

    starttime = datetime.datetime.strptime(endtime, "%Y-%m-%d") - datetime.timedelta(days=365)
    for code in cl:
        dk = KAs([code], start_time = starttime.strftime("%Y-%m-%d"), end_time = endtime)
        dk.get_k_data()
        if type(dk.data[dk.codes[0]]) == type(False): continue
        k = dk.data[dk.codes[0]]
        if len(k) < 20: continue
        dep = k[k.volume == k.volume.agg(min)]
        
        if dep.date[0] == k.iloc[[-1]].date[0]:
            if k.close.agg(min)/dep.close[0] >=0.99:
                logger.info("start...%s" % code)

#def vol_test_ai():
vol_Test()

def dd_Analyes(timezone, dd_time = -6, tr_time = 6, delay = 2, average = 15, ignore_max_day = 20, ignore = 0.1, cut_point = 0.1, before_igonre = 0.1):
    dd = EMDDScrapy()
    cl = basics.get_k_list()
    end_time = basics.k_date_now()

    df = pd.DataFrame()

    starttime = 0
    for code in cl:
        #starttime = 0
        if not os.path.exists('./data/Dadan/%s.csv' % code): 
            continue
        starttime = dd.get_latest_dd(code)
        sdd = dd.get_dd(code, starttime, timezone = timezone)
        #if datetime.datetime.strptime(sdd['time'].iloc[-1].TDATE, "%Y-%m-%d") < datetime.datetime.strptime("2016-02-16", "%Y-%m-%d"):
        #    continue
        while 1:
            if len(sdd['time']) < tr_time:
                #print sdd['time']
                starttime = sdd['time'].iloc[-1].TDATE
                starttime = datetime.datetime.strptime(starttime, "%Y-%m-%d") - datetime.timedelta(days=1)
                starttime = starttime.strftime("%Y-%m-%d")
                starttime = dd.get_latest_dd(code, starttime=starttime)
                if starttime == "": break
                sdd = dd.get_dd(code, starttime, timezone = timezone)
                if len(sdd['time']) == 0: 
                    print "have not data in there"
                    break
                continue
            else:
                break
        
        if len(sdd['time']) == 0 or starttime == "": continue
        
        starttime = sdd['time'].iloc[dd_time].TDATE
        starttime = "%s" % starttime
        ###################################
        stime_before = datetime.datetime.strptime(starttime, "%Y-%m-%d") - datetime.timedelta(days=60)        
        dk = KAs([code], start_time = stime_before.strftime("%Y-%m-%d"), end_time = end_time)
        
        dk.get_k_data()
        #print "xxxxxxxxxxx"
        #print dk.data[dk.codes[0]]
        latest_k_time = dk.data[dk.codes[0]].iloc[[0]].date[0]

        #print("%s, %s, %s" % (starttime, stime_before.strftime("%Y-%m-%d"),latest_k_time) )
        #time.sleep(10)
        #print (stime_before - datetime.datetime.strptime(latest_k_time, "%Y-%m-%d")).days
        if (stime_before - datetime.datetime.strptime(latest_k_time, "%Y-%m-%d")).days < -2:
            print("Have not data for %s" % (code))
            continue

        r = dk.rchange_k(dk.data[dk.codes[0]], starttime = stime_before, endtime = datetime.datetime.strptime(starttime, "%Y-%m-%d"))
        
        average_gap = r['average']/r['close_value']
        average_gap_v = 1 - average_gap if average_gap <= 1 else average_gap - 1
        ################################3
        if average_gap_v < before_igonre:
            print code
            r = dk.rchange_k_auto(dk.data[dk.codes[0]][dk.data[dk.codes[0]].index >= starttime], delay = delay, average = average, ignore_max_day = ignore_max_day, ignore = ignore, cut_point = cut_point)
            if type(r) == type(None):
                continue
            r['code'] = dk.codes[0]
            r['starttime'] = starttime
            df = df.append(r, ignore_index=True)
            starttime = 0
    
    if len(df) == 0: return False
    df = df.sort_values(by = 'close_rate', ascending=False)
    fname = "dd_reslut_%d.csv" % gi
    df.to_csv("dd_resule.csvaaaccccccca2")


#dd_Analyes(15)

#dd_Analyes(20, dd_time = -6, tr_time = 6, ignore_max_day = 20, ignore = 0.1, cut_point = 0.1, before_igonre = 0.1)
