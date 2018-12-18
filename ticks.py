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
from classified import Classified
import re
import k
import tradeday
from collections import OrderedDict


from pytdx.errors import TdxConnectionError, TdxFunctionCallError
from pytdx.hq import TdxHq_API, TDXParams

class TKAs:
    def __init__(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        self.path = g_data_path + "/ticks/" + today + '/'
        self.api = TdxHq_API(multithread=False, heartbeat=True,auto_retry=True, raise_exception=False)
        self.k_list = get_a_k_list()
        self.api.connect(ip='125.64.41.12')

        pass

    def __del__(self):
        self.api.disconnect()
        pass
    
    def __connect_tdx(self):
        self.api = TdxHq_API(multithread=False, heartbeat=True,auto_retry=True, raise_exception=False)
        self.api.connect(ip='125.64.41.12')

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
        date = datetime.datetime.now().strftime("%Y%m%d") if times == 'today' else times
        self.path = g_data_path + "/ticks/" + date + "/"

        if os.path.exists(self.path) == True:
            print self.path + " exist" 
            return 0
        print date + " --- " + self.path

        mkdir(self.path)
        for k in self.k_list.code:
            file_path = "%s%s.csv" % (self.path, k)
            self.refresh_ticks_tdx(k, file_path, times)


    def summary_classified_all(self):
        cf = Classified()
        if cf == None:
            print "Init the classified failed"
            return False
        
        path = g_data_path + "/ticks/"
        tlist = os.listdir(path)
        clist = cf.get_classified_list()
        
        
        for t in tlist:
            data_list = pd.DataFrame([],columns=["total_vol", 'vol_rat', 'deal_count', 'buy_count', 'sell_count', 'buy_vol', 'sell_vol', 'buy_sell_vol', 'buy_sell_rate', 'up_down_rate', 'c_name'])
            tpath = path + t
            if os.path.exists(tpath + '/summary_classified.csv') == True: continue
            
            dates = datetime.datetime.strptime(t, '%Y%m%d')
            
            for i in clist:
                ret = self.summary_classified(i, dates, cf)
                if ret == False: continue
                data_list = data_list.append(ret, ignore_index=True)
                print i

            data_list.to_csv(tpath + '/summary_classified.csv', encoding='utf-8')
            print data_list
        
        return 0

    #输入代码和时间, 提取下面的东西到同一级目录
    #总成交量, 总成交率(和总股本比), 成交次数, 买入成交量, 卖出成交量, 买入卖出比率, 资金流入流出量, 资金流入流入比率, 资金流入流出比率(和股本总量). 资金驱动力(资金流入流出和上涨下跌的比率), 上涨下跌比
    def summary_classified(self, class_name, date, cf = None):
        if cf == None: cf = Classified()
        
        
        tpath = g_data_path + "/ticks/" + date.strftime('%Y%m%d')
        
        if os.path.exists(tpath+'/summary.csv') == False: return False
        
        summary_ticks_data = pd.read_csv(tpath+'/summary.csv', dtype={'code': str})
        
        t_list = cf.get(class_name)

        tmp = pd.DataFrame([],columns=["c_name", "total_vol", 'vol_rat', 'deal_count', 'buy_count', 'sell_count', 'buy_vol', 'sell_vol', 'buy_sell_vol', 'buy_sell_rate', 'up_down_rate', 'code'])
            
        for t in t_list:
            tmp = tmp.append(summary_ticks_data[summary_ticks_data.code == t], ignore_index=True)

        #print code
        #成交总量
        sp = {'total_vol':tmp.total_vol.sum()}
        
        #总成交率
        #sp['vol_rat'] = sp['total_vol']/(base_info_df.outstanding[base_info_df.index[0]] * k_before_df.close[k_before_df.index[0]]*10000)
        sp['vol_rat'] = tmp.vol_rat.mean()
        
        #成交次数
        sp['deal_count'] = tmp.deal_count.sum()

        #买入次数
        sp['buy_count'] = tmp.buy_count.sum()

        #卖出次数
        sp['sell_count'] = tmp.sell_count.sum()

        #买入成交量
        sp['buy_vol'] = tmp.buy_vol.sum()

        #卖出成交量
        sp['sell_vol'] = tmp.sell_vol.sum()
        
        #卖出买入比率
        sp['buy_sell_rate'] = tmp.buy_sell_rate.mean()

        #资金买入卖出量
        sp['buy_sell_vol'] = tmp.buy_sell_vol.sum()
        
        #资金流入流出量
        
        #资金流入流出比率(和股本总量)
        sp['buy_sell_rate'] = tmp.buy_sell_rate.mean()

        #上涨下跌比
        sp['up_down_rate'] =  tmp.up_down_rate.mean()
        sp['c_name'] = class_name

        return sp

    #def merge_k_t(self):

    def mearge_ticks(self, timezone):
        path = g_data_path + "/ticks/"
        tlist = os.listdir(path)
        datas = pd.DataFrame()
        for t in tlist:
            tpath = path + t
            ticks_date = datetime.datetime.strptime(t, '%Y%m%d')
            print ticks_date
            if ticks_date >
            data_list = pd.DataFrame([],columns=["date":ticks_date, "total_vol", 'vol_rat', 'deal_count', 'buy_count', 'sell_count', 'buy_vol', 'sell_vol', 'buy_sell_vol', 'buy_sell_rate', 'up_deal_count_open', 'up_down_vol_close', 'up_down_count_close', 'code'])
            

            if os.path.exists(tpath + '/summary.csv') == False: continue
                
            data = pd.read_csv(tpath + '/summanry.csv', dtype={'code': str})
            datas.append(data, ignore_index=True)

        return datas
    def summary_all(self):
        path = g_data_path + "/ticks/"
        tlist = os.listdir(path)
        for t in tlist:
            
            data_list = pd.DataFrame([],columns=["total_vol", 'vol_rat', 'deal_count', 'buy_count', 'sell_count', 'buy_vol', 'sell_vol', 'buy_sell_vol', 'buy_sell_rate', 'up_deal_count_open', 'up_down_vol_close', 'up_down_count_close', 'code'])
            tpath = path + t
            print t
            dates = datetime.datetime.strptime(t, '%Y%m%d')
            print dates
            yesterday = tradeday.get_latest_tradeday(dates)
            print yesterday

            #time.sleep(5)
            #print tpath
            print dates
            if os.path.exists(tpath+'/summary.csv') == True: continue
            print tpath+'\summary.csv'
            print "-------------"
            for c in os.listdir(tpath):
                code = re.findall('(\d+).csv', c)
                print code[0]
                ret = self.summary_ticks(code[0], dates, yesterday)
                if ret == False: continue

                ret['code'] = code[0]
                data_list = data_list.append(ret,  ignore_index=True)
            data_list.to_csv(tpath + '/summary.csv')
            print data_list

        return data_list

    def get_today_key(self, code, date = 'today'):
        k_path = '%s/%s/%s_D.csv' % (g_data_path, code, code)
        if date == 'today':
            date = datetime.datetime.now()
        
        if os.path.exists(k_path) == False: return False
        k_info_df = pd.read_csv(k_path, dtype={'code': str})
        k_info_df = k_info_df[k_info_df.date == date.strftime("%Y-%m-%d")]
        return k_info_df



    #输入代码和时间, 提取下面的东西到同一级目录
    #总成交量, 总成交率(和总股本比), 成交次数, 买入成交量, 卖出成交量, 买入卖出比率, 资金流入流出量, 资金流入流入比率, 资金流入流出比率(和股本总量). 资金驱动力(资金流入流出和上涨下跌的比率), 上涨下跌比
    def summary_ticks(self, code, date, yesterday):
    
        base_info_path = g_data_path + 'stock_list.cvs'
        base_info_df = pd.read_csv(base_info_path, dtype={'code': str})
        base_info_df = base_info_df[base_info_df.code == code]

        k_path = '%s/%s/%s_D.csv' % (g_data_path, code, code)
        if os.path.exists(k_path) == False: return False

        k_info_df = pd.read_csv(k_path, dtype={'code': str})
        k_before_df = k_info_df[k_info_df.date == yesterday.strftime("%Y-%m-%d")]
        k_info_df = k_info_df[k_info_df.date == date.strftime("%Y-%m-%d")]

        if len(k_info_df) <= 0 or len(k_before_df) <= 0: return False
        ticks_path = '%s/ticks/%s/%s.csv' % (g_data_path, date.strftime("%Y%m%d"), code)
        ticks_info = pd.read_csv(ticks_path)
        
        if len(ticks_info) <= 2: return False

        #print code
        #成交总量
        sp = {'total_vol':k_info_df.volume.values[0]}
        
        #总成交率
        #sp['vol_rat'] = sp['total_vol']/(base_info_df.outstanding[base_info_df.index[0]] * k_before_df.close[k_before_df.index[0]]*10000)
        if len(base_info_df.outstanding) <= 0:
            return False

        sp['vol_rat'] = sp['total_vol']/(base_info_df.outstanding[base_info_df.index[0]] *10000)
        
        ############################################成交次数相关
        #成交次数
        sp['deal_count'] = len(ticks_info)

        #买入次数
        sp['buy_count'] = len(ticks_info[ticks_info.buyorsell == 0])

        #卖出次数
        sp['sell_count'] = len(ticks_info[ticks_info.buyorsell == 1])

        ##############################################
        if (sp['sell_count'] <= 0) or (sp['buy_count'] <= 0) or (sp['deal_count'] <= 0):
            return False
        #########################################成交量相关
        #买入成交量
        sp['buy_vol'] = ticks_info[ticks_info.buyorsell == 0 ]['vol'].sum()

        #卖出成交量
        sp['sell_vol'] = ticks_info[ticks_info.buyorsell == 1 ]['vol'].sum()
        
        #卖出买入比率
        sp['buy_sell_rate'] = sp['buy_vol']/(sp['sell_vol']+sp['buy_vol'])

        #资金买入卖出量
        sp['buy_sell_vol'] = sp['buy_vol'] - sp['sell_vol']
        
        #资金流入流出量
        
        #资金流入流出比率(和股本总量)
        sp['buy_sell_rate'] = sp['buy_sell_vol']/(base_info_df.outstanding[base_info_df.index[0]] * k_before_df.close[k_before_df.index[0]]*10000)

        #上涨下跌比-次数
        sp['up_down_count_close'] = len(ticks_info[ticks_info.price > k_before_df.close[k_before_df.index[0]]])/len(ticks_info)
        sp['up_down_vol_close'] = ticks_info[ticks_info.price > k_before_df.close[k_before_df.index[0]]]
        if len(sp['up_down_vol_close']) > 1:
            sp['up_down_vol_close'] = sp['up_down_vol_close'].price.sum()
            
        else:
            sp['up_down_vol_close'] = 0


        #################################################
        #上涨下跌比 - 开盘
        sp['up_deal_count_open'] = len(ticks_info[ticks_info.price > k_info_df.open[k_info_df.index[0]]])/len(ticks_info)
        #sp['up_deal_vol_open'] = ticks_info[ticks_info.price > k_info_df.open[k_info_df.index[0]]].sum()/len(ticks_info)
        
        #资金驱动力##########有作用成交vs无作用成交
        #sp['money_driver'] = self.money_driver(date, code)
        for indexs in ticks_info.index:
            ticks_info.loc[indexs].values[0]
            
        return sp


"""
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
                start_time = datetime.datetime.strptime(start_time.strftime("%Y-%m-%d:")+'13:00', "%Y-%m-%d:%H:%M")
            end_time = start_time + datetime.timedelta(minutes = time_area)
            tmp_data = ticks_info[(ticks_info.time >= start_time) & (ticks_info.time < end_time)]
            ret = tmp_data.vol.sum()
            result[start_time.strftime("%H:%M")] = abs(ret)/((tmp_data.price.values[-1] - before)/tmp_data.price.values[-1])
            start_time = end_time
            before = tmp_data.price.values[-1]

        print result
        return result
"""
"""    
##############################################################################
##############################################################################
#和板块相关的龙头梳理
"""
"""
    def get_summary_sort(self, t, keyword, number):
        return t.sort([keyword],ascending=True).head(number)
    

    def get_class_by_t_sort(self, t, number, save = True):
        cf = Classified()
        if cf == None:
            print "Init the classified failed"
            return False
        result_hash = {}

        for i in t.columns.values.tolist():
            result_list = self.get_summary_sort(t, i, number)
            result_hash[i] = cf.get_by_list(result_list)
            items = pd.Dataframe(columns=['code', 'class'])
            if save = True:
                for code in result_hash[i]:
                    df = pd.Dataframe('code': code, 'class': result_hash[code])
                    items = items.append(df, ignore_index=True)
                items.to_csv(self.path)


        if save == True:
            for i in result_hash()
        return result_hash

    
    
"""