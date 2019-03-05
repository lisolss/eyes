# -*- coding: utf-8 -*-
from __future__ import division
import os
import datetime
import time
import pandas as pd
import logging
import ticks
import numpy as np
from basics import *
from classified import Classified
import re
import k
import tradeday
from collections import OrderedDict
import thread 
from classified import Classified
from ticks import TKAs
from k import KAs

dd = TKAs()

def get_class_from_code(codes):
    pass

def get_top_codes(codes, top, dates, types, dk):
    datas = pd.DataFrame()
    top = int(len(codes) * top)

    datas = dk[dk.code.isin(codes)]
    """
    for code in codes:
        k_path = '%s/%s/%s_D.csv' % (g_data_path, code, code)
        if os.path.exists(k_path) == False: 
            continue
        
        k_before_df = k_info_df[k_info_df.date == dates]

        if len(k_info_df) <= 0 or len(k_before_df) <= 0: continue
        datas = datas.append(k_before_df, ignore_index=True)
    """ 
    datas = eval("datas.sort_values([\'%s\'] ,ascending=False)" % (types))
    datas = datas.head(top)

    return datas
        
def get_code_from_class(class_name = 'all', top = 0.2, types='rate', dates = 'today'):
    class_list = {}
    cf = Classified()
    code_list = get_k_list()

    dk = KAs(code_list, start_time = dates, end_time = dates)
    dk.get_k_data_pd()

    if cf == None:
        print "Init the classified failed"
        return False
    
    if class_name != 'all':
        class_list[class_name] = cf.get(class_name)
        if len(class_list[class_name]) <= 0:
            return None
    else:
        clist = cf.get_classified_list()
        for i in clist:
            code_list = cf.get(i)
            
            if len(code_list) <= 0:
                continue
            
            code_list = get_top_codes(code_list, top, dates, types, dk.data)
            class_list[i] = code_list
            #print i
            
    return class_list  


def get_code_from_file(filename):

    pass

def get_ticks_summary(codes, fromday, today, ignore_value = 15000, time_step = 10):
    ticks_data = {}
    for class_name, code_list in codes:
        
        ticks[class_name] = dd.get_ticks_summary_timezone(code_list, fromday, today, ignore_value, time_step)
    
    return ticks_data



"""
def sort_by(obj, key, types, top = ":"):
    sort_data = pd.DataFrame(columns=['class_name', 'data', 'sort'])

    for class_name,result in obj:



    if len(o) == type({}):
        datas = eval("datas.sort_values(%s)" % (types))
        datas = eval("datas[%s]" % (top))
    elif type(obj) == type(pd.DataFrame()):
        for 
    pass
"""

