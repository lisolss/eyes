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
from k import KAs
import tradeday
from collections import OrderedDict

from pytdx.errors import TdxConnectionError, TdxFunctionCallError
from pytdx.hq import TdxHq_API, TDXParams

class TKAs:
    def __init__(self, data_path, type="D"):
        self.path = g_data_path + data_path
        self.k_list = get_a_k_list()
        self.type = type
        self.data = ""
        pass
    
    def __del__(self):
        pass

    def _load_data_(self, start_time, end_time = "200", inmemory = True):
        K = KAs(self.k_list.values, start_time, end_time, inmemory)
        self.data = K.get_k_data(self.type)

    #k: k data
    #point: The k point of check
    #gap: the expect V bound percentage
    #vtimeline: how long with the bound
    def v_gap(self, k, point, deep, gap, vtimeline, goback = False):
        total_count = len(k)
        if total_count < vtimeline:
            return False
        vtimeline = vtimeline + 1
        data = k.iloc[point : point + vtimeline]
        #规定时间内最低价格是否跌破v点
        if data.close.agg(min) < (data.close[0] * 1.005): return False
        #规定时间内最高价格是否超过有效值
        if data.close.agg[max] < (data.close[0] * gap): return False
        
        data = k.iloc[point - deep: point]
        if data.close.agg(min) < data.close[-1]: retrun False
        
        retrun True

    def v_point(self, k, deep, gap, vtimeline, timeline = 0, goback = False):
        total_k = len(k)
        points = []
        if timeline != 0 and timeline > total_k: return 0
        total = timeline if timeline != 0 else total_k
        
        for i in range(0, total):
            if k.iloc[i].close() > k.iloc[i+1].close():
                continue
            else:
                if v_gap(k, i, deep, gap, vtimeline)  == True:
                    points.append(i)
                else
                    continue
        
        return points
    
    def v_line(self, k, points, line_gap = 0.01, break_time = 0):
        line = {}
        total = len(points)
        for i in range(0, total):
            for ii in range(i,total):
                line_gap = (k.iloc[points[ii]].close-k.iloc[points[i]].close())/(k.iloc[points[ii]].index() - k.iloc[points[i]].index())
                
        pass
    
    def v_layer(self, k, points, line)
