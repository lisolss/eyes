# -*- coding: utf-8 -*-
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
        self.start_time = '' if start_time == None else datetime.datetime.strptime(start_time, "%Y-%m-%d")


        #the end_time value is "yyyy-mm-dd" or "x days"
        if end_time != None:
            if type(end_time) != type(1):
                self.end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d") 
            else:
                self.end_time = self.start_time + datetime.timedelta(days=end_time) if self.start_time != None else ''
        else:
            self.end_time = '' 
        

    def get_k(self, code, type = ''):
        
        path = g_data_path + code + '.csv'
        data = pd.read_csv(path)

        data = data.set_index(date['date'])

        timezone = self.start_time + '' + self.end_time
        data = data[self.start_time:self.end_time]

        
        




