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
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.path = g_data_path + "/ticks/" + today + '/'
        mkdir(self.path)
        self.api = TdxHq_API(multithread=False, heartbeat=True,auto_retry=True, raise_exception=False)
        self.api.connect(ip='125.64.41.12')
        pass
    def __del__(self):
        self.api.disconnect()
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
        
    #def refresh_tick_data_tdx(self, code, date, path):
        

    def refresh_all_ticks(self, times = 'today'):
        self.k_list = get_a_k_list()
        for k in self.k_list.code:
            file_path = "%s%s.csv" % (self.path, k)
            self.refresh_ticks_tdx(k, file_path, times)
        