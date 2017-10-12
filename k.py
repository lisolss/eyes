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
        self.path = './data/'
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
        

    def get_k(self, code, type = ''):
        
        path = g_data_path + code + '.csv'
        data = pd.read_csv(path)

        data = data.set_index(data['date'])
        data = data[self.start_time.strftime("%Y-%m-%d"):self.end_time.strftime("%Y-%m-%d")]
        
        return data

    def get_k_data(self, type=''):
        for code in self.codes:
            self.data[code] = self.get_k(code, type)
        

    """
    return: buy, top, dep, average, top_day, dep_day, close_value
    """
    def rchange_k_auto(self, k, delay = 1, average = 5, ignore = 0.05, ignore_max_day = 10):
    
        #Get delay top value
        k_delay = k.iloc[:delay+1]
        delay_top_v = k_delay[k_delay.close == k_delay.close.agg(max)]
    
        r = {}
        #Get the avagerage_line
        r['buy'] = delay_top_v.close[0]
        print delay_top_v

        print "top is %d" % (r['buy'])
        corss_line = 0
        current_gap = 0

        total_count = len(k)
        if total_count <= average: return None
        lastday = 0

        for i in range(0, total_count):
            st_point = i - average if i >= average else 0
            av_point = i+1  

            k_t = k.iloc[st_point:av_point].close.mean()
            last_gap = current_gap
            
            current_gap = k.iloc[[i]].close[0] - k_t
            if current_gap > 0 and last_gap <= 0:
                corss_line = 1
            elif current_gap <0 and last_gap >= 0:
                corss_line = -1
            else:
                corss_line = 0
            lastday = i
    
            ###设定忽略交叉点的幅度, 避免小范围波动的交叉噪音###
            if corss_line != 0:
                cv = k.iloc[[i]].close[0]/r['buy']
                rcv = 1 - cv if cv <= 0 else cv-1

                if rcv > ignore:
                    r['last_day'] = (datetime.datetime.strptime(k.iloc[[i]].index[0], "%Y-%m-%d") - self.start_time).days
                    r['close_value'] = k.iloc[[i]].close[0]
                    r['close_rate'] = cv - 1
                    r['average'] = k.close[:i].mean()
                    break
                #elif (datetime.datetime.strptime(k.iloc[[i]].index[0], "%Y-%m-%d") - self.start_time).days > ignore_max_day:
                elif i > ignore_max_day:
                    r['last_day'] = (datetime.datetime.strptime(k.iloc[[i]].index[0], "%Y-%m-%d") - self.start_time).days
                    r['close_value'] = k.iloc[[i]].close[0]
                    r['close_rate'] = cv - 1
                    r['average'] = k.close[:i].mean()
                    break

        ############################################################
        k = k.iloc[:lastday]
        top = k[k.close == k.close.agg(max)]
        top_date = top.index[0]
        r['top'] = top.close[0]/r['buy'] - 1

        dep = k[k.close == k.close.agg(min)]
        dep_date = dep.index[0]
        r['dep'] = dep.close[0]/r['buy'] - 1
        print "xxxxx%f" % r['dep']

        #get the day
        r['top_day'] = (datetime.datetime.strptime(top_date, "%Y-%m-%d") - self.start_time).days
        r['dep_day'] = (datetime.datetime.strptime(dep_date, "%Y-%m-%d") - self.start_time).days
        
        return r

        
        
        




