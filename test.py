# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import traceback
import re
import time
import datetime
import sys

date = datetime.datetime.now().strftime("%Y%m%d")
cvs_lastest = "2017-08-30"
l = datetime.datetime.strptime(cvs_lastest, "%Y-%m-%d")
date = l.strftime("%Y%m%d")
print date



l = datetime.datetime.now()
for i in range(100):
    l = l - datetime.timedelta(days=1)
    cvs_lastest = l.strftime("%Y%m%d")
    print cvs_lastest

exit()

import tushare as ts
import pandas as pd
import numpy as np

from collections import OrderedDict
from pytdx.errors import TdxConnectionError, TdxFunctionCallError
from pytdx.hq import TdxHq_API, TDXParams


api = TdxHq_API(multithread=False, heartbeat=True,auto_retry=True, raise_exception=False)
api.connect(ip='125.64.41.12')
"""
print api.get_security_count(TDXParams.MARKET_SH)
#stocks = api.get_security_list(0, 100000)
data = pd.concat([pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(sse='sz' if j == 0 else 'sh').set_index(
            ['code', 'sse'], drop=False) for i in range(int(api.get_security_count(j) / 1000) + 1)], axis=0) for j in range(2)], axis=0)
data.to_csv('./xxx.csv', encoding='utf-8')
print data

api.disconnect()

exit()
for i in range(20):
    print i

    count = i*1000
    print count
    time.sleep(2)
    dd = api.get_security_list(0, count)
    for i in dd:
        print i['code']

api.disconnect()

exit()
print dd
for i in dd:
    for i1 in i:
        print i1['code']
    break
exit()
api.disconnect()
assert stocks is not None
assert type(stocks) is list
assert len(stocks) > 0
for i in stocks:
    print i['code']
exit()
print stocks
exit()"""

print("查询分时行情")
#data = api.get_transaction_data
#api.get_history_transaction_data()
data2 = api.to_df(api.get_history_transaction_data(TDXParams.MARKET_SH, '600600', 0, 0, 20170309))
for i in range(1000):
    
    data = api.to_df(api.get_history_transaction_data(TDXParams.MARKET_SH, '600600', i*100, 100, 20170309))
    data2 = pd.concat([data, data2])
    if len(data) <= 99:
        break
    #time.sleep(1)
api.disconnect()
print data2 
exit()

#data = api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 30)
#data = api.get_minute_time_data(TDXParams.MARKET_SH, '600300')
#data = api.get_history_minute_time_data(TDXParams.MARKET_SH, '600300', 20161209)

assert data is not None
data = api.to_df(data)
print type(data)
print data
print "finished"
exit()

df = ts.get_today_ticks('600600')
print df
exit()

dates = ['2011-2-30','2011-2-1','2012-3-1']
ts = pd.DataFrame([1,2,"哈哈",6,7,"哈哈", "aaa", "aaa"],columns=["aaa"])



ts3 = pd.DataFrame([1,2,5,6,7,8,1,2,3],columns=["bbb"])

ts2 = pd.DataFrame()
ts2 = ts2.append(ts, ignore_index=True)
ts2 = ts2.append(ts3, ignore_index=True)

print ts2.drop_duplicates("aaa")
#print sys.argv[1]
s = "2017-08-29"
a = datetime.datetime.strptime(s, "%Y-%m-%d")

b = datetime.datetime.now()

print "tttttttttttttt"
print (a - b).days

def k_date_now(a = None):
    now = datetime.datetime.now()
    print a
    if a != None: now = now - datetime.timedelta(a)
    today = now.strftime("%Y-%m-%d")
    print("date is " + today)
    return today

print k_date_now(1)

print sys.path[0]

exit()
a = "2017-10-09 10:50"

b = a.split(' ')[0]
print b

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
"""
tx = getHTMLText("http://data.eastmoney.com/zjlx/detail.html")

pattern = re.compile('dataurl.*token=(\d|\w+)\{')
res = re.search(pattern, tx)
print res.group(1)
"""


def format_data(arrays, indexs = None, columnss = None):
    data = zip(*[iter(arrays)]*len(columnss))
    df = pd.DataFrame(data, index=indexs, columns=columnss)
    try:
        if df.empty:
            print("Error: did not get the format data")
            return ''
    except:
        return ''
    print df

#dd = format_data([1, 2, 3, 4, 5, 6, 7, 8], indexs = list("xy"),columnss = list("abcd"))
#print dd

class WebScrapy:

    def __init__(self, name, **age):
        self.name = name
        for key in age.keys():
            exec("self.%s = \'%s\'" % (key, age[key]))

        print self.test
        print self.test2

k = {'test':'ooo', 'test2':'o\d\p...oo2'}
a = WebScrapy("test", **k)
print "测试"

k = [1, 2, 4, 5, 6, 7, 8]
k1 = k[1:]
print k1
"""
aaa = 'var sRcSWRth={pages:71,date:"2014-10-22",data:["2,300699,光威复材,79.09,10.00,60566.70,19.80,49135.50,16.06,11431.20,3.74,-14575.54,-4.76,-45991.15,-15.03,2017-09-28 14:43:06","2,000725,京东方A,4.50,7.14,23649.63,4.22,43602.57,7.78,-19952.95,-3.56,-6786.81,-1.21,-16862.82,-3.01,2017-09-28 14:43:06","2,000858,五粮液,57.57,1.53,23577.40,15.17,28023.84,18.03,-4446.44,-2.86,-16523.46,-10.63,-7053.95,-4.54,2017-09-28 14:43:06","2,000868,安凯客车,9.56,10.01,22178.55,13.33,26017.70,15.63,-3839.16,-2.31,-12323.67,-7.41,-9854.88,-5.92,2017-09-28 14:43:06","2,000786,北新建材,16.90,4.77,22119.01,23.65,16988.22,18.16,5130.79,5.49,-11117.40,-11.89,-11001.61,-11.76,2017-09-28 14:43:06","1,603019,中科曙光,36.87,9.99,21422.69,9.40,25956.57,11.39,-4533.88,-1.99,-13068.69,-5.74,-8354.00,-3.67,2017-09-28 14:43:06","2,002467,二六三,8.93,9.98,14851.91,42.78,13129.96,37.82,1721.94,4.96,-7410.85,-21.35,-7441.06,-21.43,2017-09-28 14:42:07","2,000768,中航飞机,19.12,1.76,14417.72,24.77,11167.77,19.18,3249.95,5.58,-5829.15,-10.01,-8588.57,-14.75,2017-09-28 14:43:06","2,000559,万向钱潮,12.07,4.68,13209.44,18.35,9815.50,13.63,3393.94,4.71,-5262.96,-7.31,-7946.48,-11.04,2017-09-28 14:43:06","2,002024,苏宁云商,13.09,5.56,12165.31,10.90,12945.41,11.60,-780.09,-0.70,-3066.05,-2.75,-9099.26,-8.15,2017-09-28 14:42:07","2,002049,紫光国芯,35.88,6.00,11820.31,8.95,14722.55,11.15,-2902.24,-2.20,-9268.27,-7.02,-2552.04,-1.93,2017-09-28 14:42:07","2,300527,华舟应急,22.82,9.92,11324.77,22.53,11983.18,23.84,-658.42,-1.31,-5134.08,-10.21,-6190.68,-12.32,2017-09-28 14:43:06","2,000050,深天马A,22.70,2.85,10282.10,14.59,8294.29,11.77,1987.81,2.82,-4949.44,-7.02,-5332.66,-7.57,2017-09-28 14:43:06","2,000848,承德露露,10.15,4.96,10277.57,22.54,6873.86,15.08,3403.70,7.47,-3234.69,-7.09,-7042.88,-15.45,2017-09-28 14:43:06","2,000799,酒鬼酒,29.02,4.77,10064.46,12.91,6922.95,8.88,3141.51,4.03,-3101.26,-3.98,-6963.20,-8.93,2017-09-28 14:43:06","1,600206,有研新材,11.92,4.65,9570.06,9.06,11809.31,11.18,-2239.25,-2.12,-5778.79,-5.47,-3791.27,-3.59,2017-09-28 14:43:06","2,002123,梦网集团,12.12,9.98,9262.88,25.24,10017.74,27.30,-754.86,-2.06,-4122.21,-11.23,-5140.67,-14.01,2017-09-28 14:42:07","2,300697,电工合金,38.88,9.99,8636.31,10.58,5129.40,6.28,3506.91,4.30,2228.09,2.73,-10864.40,-13.31,2017-09-28 14:43:06","2,000960,锡业股份,15.70,2.01,8593.15,10.31,7415.63,8.89,1177.52,1.41,-2891.53,-3.47,-5701.62,-6.84,2017-09-28 14:43:06","1,603386,广东骏亚,28.20,9.98,8546.18,29.23,9150.41,31.30,-604.23,-2.07,922.88,3.16,-9469.06,-32.39,2017-09-28 14:43:06","2,000826,启迪桑德,35.78,2.05,8352.19,21.62,6117.96,15.83,2234.22,5.78,-3819.71,-9.89,-4532.48,-11.73,2017-09-28 14:43:06","1,600038,中直股份,43.75,3.94,8296.59,19.21,3489.26,8.08,4807.32,11.13,-4297.80,-9.95,-3998.79,-9.26,2017-09-28 14:43:06","2,002456,欧菲光,21.25,1.19,8272.43,12.58,4499.69,6.84,3772.75,5.74,-3897.25,-5.93,-4375.19,-6.65,2017-09-28 14:42:07","1,601012,隆基股份,29.48,8.22,8018.48,7.15,6480.81,5.78,1537.68,1.37,-5461.82,-4.87,-2556.67,-2.28,2017-09-28 14:43:06","2,300618,寒锐钴业,197.22,6.78,7440.41,11.09,4605.61,6.86,2834.80,4.23,-4554.29,-6.79,-2886.12,-4.30,2017-09-28 14:43:06","1,600887,伊利股份,26.44,3.93,7298.15,5.20,9516.87,6.78,-2218.71,-1.58,-5249.28,-3.74,-2048.87,-1.46,2017-09-28 14:43:06","2,300418,昆仑万维,26.15,2.55,7259.48,18.52,2328.04,5.94,4931.44,12.58,-2824.09,-7.20,-4435.39,-11.32,2017-09-28 14:43:06","1,600703,三安光电,23.14,4.52,6943.01,8.31,9214.20,11.03,-2271.19,-2.72,-6299.55,-7.54,-643.46,-0.77,2017-09-28 14:43:06","2,300077,国民技术,15.69,2.15,6928.31,7.66,6936.93,7.67,-8.62,-0.01,-5201.95,-5.75,-1726.36,-1.91,2017-09-28 14:43:06","1,603799,华友钴业,91.28,2.41,6595.77,4.11,7261.43,4.53,-665.66,-0.41,-5025.46,-3.13,-1570.31,-0.98,2017-09-28 14:43:06","2,300251,光线传媒,10.78,4.15,6509.51,15.54,3876.08,9.26,2633.43,6.29,-2238.58,-5.35,-4270.93,-10.20,2017-09-28 14:43:06","2,300055,万邦达,19.80,2.43,6414.61,6.71,6961.07,7.28,-546.46,-0.57,-2851.11,-2.98,-3563.50,-3.73,2017-09-28 14:43:06","1,600519,贵州茅台,518.80,2.08,6392.88,5.40,7667.31,6.48,-1274.43,-1.08,-6110.68,-5.16,-282.21,-0.24,2017-09-28 14:43:06","2,002511,中顺洁柔,13.95,3.18,6319.60,31.37,4957.41,24.61,1362.19,6.76,-3106.06,-15.42,-3213.54,-15.95,2017-09-28 14:42:07","2,002192,融捷股份,42.67,5.10,6271.01,11.13,5785.39,10.27,485.63,0.86,-3768.65,-6.69,-2502.37,-4.44,2017-09-28 14:42:07","2,002148,北纬科技,12.19,3.22,6148.68,18.94,4768.57,14.69,1380.11,4.25,-2658.79,-8.19,-3489.90,-10.75,2017-09-28 14:42:07","1,601166,兴业银行,17.37,-0.06,5758.98,7.45,3955.30,5.12,1803.68,2.33,-6680.57,-8.64,921.60,1.19,2017-09-28 14:43:06","1,601398,工商银行,6.02,0.00,5398.98,7.94,4787.31,7.04,611.67,0.90,-5081.91,-7.48,-317.07,-0.47,2017-09-28 14:43:06","2,000423,东阿阿胶,65.08,2.09,5241.05,11.81,2660.91,5.99,2580.14,5.81,-2317.12,-5.22,-2923.93,-6.59,2017-09-28 14:43:06","1,600196,复星医药,33.97,3.06,5144.76,11.05,6129.93,13.17,-985.16,-2.12,-3731.16,-8.02,-1413.60,-3.04,2017-09-28 14:43:06","2,000823,超声电子,15.00,4.09,5098.80,14.94,3308.44,9.69,1790.36,5.24,76.90,0.23,-5175.70,-15.16,2017-09-28 14:43:06","2,002304,洋河股份,103.40,3.09,5065.75,9.72,5443.51,10.45,-377.76,-0.72,-4942.39,-9.48,-123.36,-0.24,2017-09-28 14:42:07","2,002241,歌尔股份,20.38,1.09,4789.37,11.20,3793.21,8.87,996.16,2.33,-3550.33,-8.30,-1239.04,-2.90,2017-09-28 14:42:07","1,601328,交通银行,6.33,-0.16,4655.73,16.09,4954.03,17.12,-298.29,-1.03,-4518.41,-15.61,-137.32,-0.47,2017-09-28 14:43:06","2,300589,江龙船艇,31.23,10.00,4619.60,25.87,5095.30,28.54,-475.70,-2.66,-2512.78,-14.07,-2106.82,-11.80,2017-09-28 14:43:06","2,002570,贝因美,10.29,3.00,4599.38,13.60,2920.29,8.64,1679.09,4.96,-848.06,-2.51,-3751.32,-11.09,2017-09-28 14:42:07","2,300098,高新兴,14.31,3.47,4480.58,18.15,2507.84,10.16,1972.73,7.99,-1407.86,-5.70,-3072.72,-12.45,2017-09-28 14:43:06","2,000957,中通客车,14.69,5.00,4433.49,7.12,4241.42,6.81,192.07,0.31,-2573.67,-4.13,-1859.82,-2.99,2017-09-28 14:43:06","2,002065,东华软件,11.26,2.18,4415.20,9.17,4453.55,9.25,-38.35,-0.08,-1933.46,-4.02,-2481.74,-5.16,2017-09-28 14:42:07","2,002885,京泉华,43.10,5.38,4278.40,19.72,3024.74,13.94,1253.66,5.78,-2502.93,-11.54,-1775.47,-8.18,2017-09-28 14:42:07"]}'

#bb = re.findall('([\d\-\:][^"]+),', aaa)
bb = re.findall('([\d\:\-\.]+),', aaa)
print bb[0]
for i in bb:
    print i

a = eval(bb[0])
s=0
for i in a:
    s=s+1
    print s
    print i

a = list("2,33,5.5,22")
for i in a:
    print i
    """

s = "2017-08-29"
a = datetime.datetime.strptime(s, "%Y-%m-%d")

b = datetime.datetime.now()

print "tttttttttttttt"
print (b - a).days

cvs_lastest = "2017-08-30"

l = datetime.datetime.now
for i in range(100):
    l = l - datetime.timedelta(days=1)
    cvs_lastest = l.strftime("%Y%m%d")
    print cvs_lastest

print "d = %s" % (cvs_lastest)

from datetime import datetime

dates = ['2011-2-30','2011-2-1','2012-3-1']
ts = pd.DataFrame([1,2,"哈哈",6,7,"哈哈", "aaa", "aaa"],columns=["aaa"])



ts3 = pd.DataFrame([1,2,5,6,7,8,1,2,3],columns=["bbb"])

ts2 = pd.DataFrame()
ts2 = ts2.append(ts, ignore_index=True)
ts2 = ts2.append(ts3, ignore_index=True)


ts2.to_csv('./xxx.test',encoding='utf-8')
ts2 = pd.read_csv('./xxx.test')
print ts2.aaa
print ts2[ts2.aaa == 'aaa'].bbb

hs = [{"a":"1", "c":"2"}, {"c":"3", "a":"4"}]
pd = pd.DataFrame(hs)
print pd

url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=TDATE&sr=-1&p=1&ps=50&filter=(SECUCODE=%27600600%27)&js=var%20UObvwgvJ={pages:(tp),data:(x)}&type=DZJYXQ&rt=50253591'

a = re.sub('filter=\(SECUCODE=.*\)\&', '', url)
print a
exit()
del ts2['bbb']
print ts2
print 'fffffffffffff'

ts2 = pd.DataFrame(ts2.aaa, columns=['aaa'])
print ts2
exit()

ts2 = ts2.fillna(0)
#print ts
print "xxx"

#b = ts.set_index(ts['aaa'])
#b = b.drop(b.index[1])
#print b
#a = ts[ts.columns(["aaa"]['2013-2-1':'2013-3-1']]
#print a
print ts2
close()
p = '2011-2-1'
p1  = '2013-3-1'
a = ts.iloc[0:1]
print ts.mean()
print a
print "gggg"
print list(ts)
a = ts[ts.aaa == ts.aaa.agg(min)]
print a
print a.index[0]
if a.index[0] < ts.index[1]:
    print "hahah"
#.index(ts.aaa.agg(max))
print len(ts)

#print a.index(ts.aaa.agg(max))

"""

import logging  
import logging.handlers  
  
LOG_FILE = 'tst.log'  
"""
"""
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)   # 实例化formatter  
handler.setFormatter(formatter)      # 为handler添加formatter  
  
logger = logging.getLogger('tst')    # 获取名为tst的logger  
logger.addHandler(handler)           # 为logger添加handler  
logger.setLevel(logging.DEBUG)  
  
logger.info('first info message')  
logger.debug('first debug message')  

"""
"""
fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s')

ch = logging.StreamHandler()

logger = logging.getLogger('slogger')

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


print "logger"
logger.info("Init finished")

k_type = "30"

if not (k_type.isdigit()):
    print "aaaaa"
else:
    print "bbbb"




a = '[{"test":"1","test2":"2"},{"test3":"13","test4":"23"}]'
print a
b = eval(a)
print b[0]["test2"]

"""

print 1/2

