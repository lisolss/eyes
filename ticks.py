# -*- coding: utf-8 -*-
from __future__ import division
import os
import datetime
import time
import pandas as pd
import logging
import numpy as np
import tushare as ts
from basics import *

from collections import OrderedDict


from pytdx.errors import TdxConnectionError, TdxFunctionCallError
from pytdx.hq import TdxHq_API, TDXParams

class TKAs:
    def __init__(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        self.path = g_data_path + "/ticks/" + today + '/'
        #self.api = TdxHq_API(multithread=False, heartbeat=True,auto_retry=True, raise_exception=False)
        #self.api.connect(ip='125.64.41.12')
        pass

    def __del__(self):
        #self.api.disconnect()
        pass

    def refresh_today_ticks_ts(self, code, path):
        df = ts.get_today_ticks(code)
        df.to_csv(path, encoding='utf-8')
    
    def get_code_detail(self, code):
        return self.k_list[self.k_list.code == code]

    def refresh_tick_data_ts(self, code, date, path):
        df = ts.get_tick_data(code, date)
        df.to_csv(path,encoding='utf-8')
    

    def refresh_ticks_tdx(self, code, path, date =  'today'):
        date = datetime.datetime.now().strftime("%Y%m%d") if date == 'today' else date
        self.path = g_data_path + "/ticks/" + date + '/'
        mkdir(self.path)
        
        print code
        data = self.get_code_detail(code).sse
        code_see = TDXParams.MARKET_SH if data[data.index[0]] == 'sh' else TDXParams.MARKET_SZ
        
        data2 = self.api.to_df(self.api.get_history_transaction_data(code_see, code, 0, 0, date))
        for i in range(1000):
            data = self.api.to_df(self.api.get_history_transaction_data(code_see, code, i*1000, 1000, date))
            data2 = pd.concat([data, data2])
            if len(data) <= 999:
                break
    
        data2.to_csv(path, encoding='utf-8')
        return data2

    def refresh_all_ticks(self, times = 'today'):
        self.k_list = get_a_k_list()
        date = datetime.datetime.now().strftime("%Y%m%d") if times == 'today' else times
        self.path = g_data_path + "/ticks/" + date + '/'
        mkdir(self.path)
        for k in self.k_list.code:
            file_path = "%s%s.csv" % (self.path, k)
            self.refresh_ticks_tdx(k, file_path, times)
        

    #输入代码和时间, 提取下面的东西到同一级目录
    #总成交量, 总成交率(和总股本比), 成交次数, 买入成交量, 卖出成交量, 买入卖出比率, 资金流入流出量, 资金流入流入比率, 资金流入流出比率(和股本总量). 资金驱动力(资金流入流出和上涨下跌的比率), 上涨下跌比
    def summary_ticks(self, code, date):
        
        yesterday = date - datetime.timedelta(days=1)

        base_info_path = g_data_path + 'stock_list.cvs'
        base_info_df = pd.read_csv(base_info_path, dtype={'code': str})
        base_info_df = base_info_df[base_info_df.code == code]

        k_path = '%s/%s/%s_D.csv' % (g_data_path, code, code)
        k_info_df = pd.read_csv(k_path, dtype={'code': str})
        k_before_df = k_info_df[k_info_df.date == yesterday.strftime("%Y-%m-%d")]
        k_info_df = k_info_df[k_info_df.date == date.strftime("%Y-%m-%d")]

        ticks_path = '%s/ticks/%s/%s.csv' % (g_data_path, date.strftime("%Y%m%d"), code)
        ticks_info = pd.read_csv(ticks_path)

        #成交总量
        sp = {'total_vol':k_info_df.volume[k_info_df.index[0]]}
        
        #总成交率
        #sp['vol_rat'] = sp['total_vol']/(base_info_df.outstanding[base_info_df.index[0]] * k_before_df.close[k_before_df.index[0]]*10000)
        sp['vol_rat'] = sp['total_vol']/(base_info_df.outstanding[base_info_df.index[0]] *10000)
        
        #成交次数
        sp['deal_count'] = len(ticks_info)

        #买入次数
        sp['buy_count'] = len(ticks_info[ticks_info.buyorsell == 0])

        #卖出次数
        sp['sell_count'] = len(ticks_info[ticks_info.buyorsell == 1])

        #买入成交量
        sp['buy_vol'] = ticks_info[ticks_info.buyorsell == 0 ]['vol'].sum()

        #卖出成交量
        sp['sell_vol'] = ticks_info[ticks_info.buyorsell == 1 ]['vol'].sum()
        
        #卖出买入比率
        sp['buy_sell_rate'] = sp['buy_vol']/sp['sell_vol']

        #资金买入卖出量
        sp['buy_sell_vol'] = sp['buy_vol'] - sp['sell_vol']
        
        #资金流入流出量
        
        #资金流入流出比率(和股本总量)
        sp['buy_sell_rate'] = sp['buy_sell_vol']/(base_info_df.outstanding[base_info_df.index[0]] * k_before_df.close[k_before_df.index[0]]*10000)

        #上涨下跌比
        sp['up_down_rate'] = len(ticks_info[ticks_info.price > k_before_df.close[k_before_df.index[0]]])/ \
            len(ticks_info[ticks_info.price <= k_before_df.close[k_before_df.index[0]]])
        print sp
        #资金驱动力
        sp['money_driver'] = self.money_driver(date, code)


    def money_driver(self, date, code, time_area = 30, start_time = 0):
        ticks_path = '%s/ticks/%s/%s.csv' % (g_data_path, date.strftime("%Y%m%d"), code)
        ticks_info = pd.read_csv(ticks_path)

        yesterday = date - datetime.timedelta(days=1)
        k_path = '%s/%s/%s_D.csv' % (g_data_path, code, code)
        k_info_df = pd.read_csv(k_path, dtype={'code': str})
        k_before_df = k_info_df[k_info_df.date == yesterday.strftime("%Y-%m-%d")]
        k_info_df = k_info_df[k_info_df.date == date.strftime("%Y-%m-%d")]
        ticks_info['time'] = pd.to_datetime(ticks_info['time'])
        start_time = ticks_info.time[0] + datetime.timedelta(minutes=start_time)
        ticks_info = ticks_info[ticks_info.time >= start_time]
        result = {}
        before = k_before_df.close.values[0]
        
        while(True):
            if ticks_info.time[ticks_info.index[-1]] < start_time: break
            if start_time.hour >= 12 and start_time.hour < 13: 
                print "xxxxxxxxx"
                start_time = datetime.datetime.strptime(start_time.strftime("%Y-%m-%d:")+'13:00', "%Y-%m-%d:%H:%M")
                print start_time

            end_time = start_time + datetime.timedelta(minutes = time_area)
            tmp_data = ticks_info[(ticks_info.time >= start_time) & (ticks_info.time < end_time)]
            ret = tmp_data.vol.sum()
            result[start_time.strftime("%H:%M")] = abs(ret)/((tmp_data.price.values[-1] - before)/tmp_data.price.values[-1])
            start_time = end_time
            before = tmp_data.price.values[-1]

        print result
        return result




