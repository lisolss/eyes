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

class KAs:
    def __init__(self, code_list = None, start_time = None, end_time = None, filepath = './data/'):
        self.codes = code_list
        self.path = g_data_path
        self.data = {}
        self.start_time = None if start_time == None else datetime.datetime.strptime(start_time, "%Y-%m-%d")

        #the end_time value is "yyyy-mm-dd" or "x days"
        if end_time != None:
            if type(end_time) != type(1):
                self.end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d") 
            else:
                self.end_time = self.start_time + datetime.timedelta(days=end_time) if self.start_time != None else None
        else:
            self.end_time = None 
        

    def get_k(self, code, types = 'D'):
        path = "%s/%s/%s_%s.csv" % (g_data_path, code, code, types)
        if not os.path.exists(path):
            return False
        data = pd.read_csv(path)

        data = data.set_index(data['date'])
        data = data[self.start_time.strftime("%Y-%m-%d"):self.end_time.strftime("%Y-%m-%d")]
        
        return data

    def get_k_data(self, type='D'):
        for code in self.codes:
            self.data[code] = self.get_k(code, type)
        
    #Get the buy date and value
    def get_buy_date(self, k, delay = 1, max_ris = 0.05):
        total_count = len(k)
        if total_count <= delay: return None
        
        k_delay = k.iloc[:delay+1]
        delay_top_v = k_delay[k_delay.close == k_delay.close.agg(max)]

        k_start = k.iloc[[0]]

        gap = delay_top_v.close[0]/k_start.close[0]
        max_ris = max_ris + 1

        if gap > max_ris:
            return {}
    
        return {'buy':delay_top_v.close[0], 'buy_date':delay_top_v.index[0]}

    """
    return: buy, top, dep, average, top_day, dep_day, close_value
    Parameter:
        k: The K data
        delay: choice the buy date which top in latest $ day
        average: average line days
        ignore: ignore the wave of 
    """
    def rchange_k_auto(self, k, delay = 1, average = 5, ignore = 0.05, ignore_max_day = 10, up_igonre = 1, cut_point = 0.05, max_ris = 0.05):    
        #Get delay top value
        total_count = len(k)
        if total_count <= average: return None
        
        r = self.get_buy_date(k, delay=delay, max_ris=max_ris)
        if r == {}:
            return None

        corss_line = 0
        current_gap = 0
        lastday = 0

        for i in range(0, total_count):
            st_point = i - average if i >= average else 0
            av_point = i+1  

            k_t = k.iloc[st_point:av_point].close.mean()
            last_gap = current_gap

            #计算交叉点            
            current_gap = k.iloc[[i]].close[0] - k_t
            if current_gap > 0 and last_gap <= 0:
                corss_line = 1
            elif current_gap <0 and last_gap >= 0:
                corss_line = -1
            else:
                corss_line = 0
            lastday = i

            #取得偏离比率
            cv = k.iloc[[i]].close[0]/r['buy']
            rcv = 1 - cv if cv <= 1 else cv-1

            if k.iloc[[i]].index[0] <= r['buy_date']:
                continue

            #止损点触发
            if rcv > cut_point: 
                break
            
            ###设定忽略交叉点的幅度, 避免小范围波动的交叉噪音###
            if corss_line != 0:
                #忽略盈利状态的横盘向上交叉
                if up_igonre == 1 and cv > 1 and corss_line == 1: continue

                if rcv > ignore:
                    if k.iloc[[i]].index[0] <= r['buy_date']:
                        continue
                        
                    break
                #elif (datetime.datetime.strptime(k.iloc[[i]].index[0], "%Y-%m-%d") - self.start_time).days > ignore_max_day:
                elif i > ignore_max_day:
                    break
        
        r['last_day'] = (datetime.datetime.strptime(k.iloc[[lastday]].index[0], "%Y-%m-%d") - self.start_time).days
        r['close_value'] = k.iloc[[lastday]].close[0]
        r['close_rate'] = cv - 1
        r['average'] = k.close[:lastday].mean()
        r['close_date'] = k.iloc[[lastday]].index[0]

        ############################################################
        k = k.iloc[:lastday + 1]
        top = k[k.close == k.close.agg(max)]
        r['top_date'] = top.index[0]
        r['top'] = top.close[0]/r['buy'] - 1

        dep = k[k.close == k.close.agg(min)]
        r['dep_date'] = dep.index[0]
        r['dep'] = dep.close[0]/r['buy'] - 1

        #get the day
        r['top_day'] = (datetime.datetime.strptime(r['top_date'], "%Y-%m-%d") - self.start_time).days
        r['dep_day'] = (datetime.datetime.strptime(r['dep_date'], "%Y-%m-%d") - self.start_time).days
        
        return r
    

    #need test
    def rchange_k(self, k, starttime = 0, endtime = 0):

        if starttime == 0 or endtime == 0 :
            k = k[starttime.strftime("%Y-%m-%d"):endtime.strftime("%Y-%m-%d")]
            starttime = k.index[0]
            endtime = k.index[-1]
        r = {}
        #Get the avagerage_line
        r['buy'] = k.close[0]
        r['buy_date'] = k.index[0]
        
        r['last_day'] = (endtime - starttime).days
        r['close_value'] = k.ix[endtime.strftime("%Y-%m-%d")].close
        r['close_rate'] =  r['close_value']/r['buy'] - 1
        r['average'] = k.close.mean()
        r['close_date'] = endtime.strftime("%Y-%m-%d")

        ############################################################
        top = k[k.close == k.close.agg(max)]
        r['top_date'] = top.index[0]
        r['top'] = top.close[0]/r['buy'] - 1

        dep = k[k.close == k.close.agg(min)]
        r['dep_date'] = dep.index[0]
        r['dep'] = dep.close[0]/r['buy'] - 1

        #get the day
        r['top_day'] = (datetime.datetime.strptime(r['top_date'], "%Y-%m-%d") - starttime).days
        r['dep_day'] = (datetime.datetime.strptime(r['dep_date'], "%Y-%m-%d") - starttime).days
        
        return r

    #def k_form(dk, ignore = 0.1):
        
   #def get_vol(k, starttime, endtime):
