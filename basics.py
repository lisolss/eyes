# -*- coding: utf-8 -*-
import os
import datetime
import time
import pandas as pd
import logging
import numpy as np
import tushare as ts
import logging.handlers  
import os

g_data_path = './data/'
LOG_FILE = './test.log'
logger = logging.getLogger('slogger')



#init log system and parameter
def init():
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

"""
codelist: the code list which will refresh k data
k: use hist or k for refresh k data
ktype: which k data need. include D(daily), W(weekly), M(month), 15, 5, 30, 60
"""
def refresh_k_data(code_list, k = None, k_type = 'D'):
    logger.info("get_k_data start...")
    today = k_date_now()
    for code in code_list:
        st_name = g_data_path + code + '.csv' if k_type == 'D' else g_data_path + code + "_" + k_type+'.cvs'
        
        logger.debug("path is " + st_name)
        data = None
        
        if os.path.exists(st_name):
            csv_data = pd.read_csv(st_name)
            csv_latest = csv_data.date
            csv_latest = csv_latest.iloc[-1] if not k_type.isdigit() else csv_latest.iloc[-1].split(" ")[0]
            
            #get the latest date
            l = datetime.datetime.strptime(csv_latest, "%Y-%m-%d")
            l = l + datetime.timedelta(days=1)
            csv_lastest = l.strftime("%Y-%m-%d")

            if csv_latest == today:
                logger.debug(st_name + " have alrealy")
                continue
        
            logger.debug(csv_latest + " -- " + today)

            data = ts.get_k_data(code, start = csv_latest, end = today, ktype=k_type ) if (k == "yes") else ts.get_hist_data(code, start = csv_latest, end = today, ktype = k_type)
            try:
                if data.empty or data.shape[0] < 1:
                    logger.debug("Error: did not get the data")
                    continue
            except:
                continue
            
            data = data.sort_index(ascending=True)
            #data = data.drop(data.index[0])
            data.to_csv(st_name, mode = 'a', header=None)
        
        else:

            data = ts.get_k_data(code, ktype=k_type) if (k) else ts.get_hist_data(code, ktype=k_type)
            try:
                if data.empty:
                    logger.debug("Error: did not get the data")
                    continue
            except:
                continue
        
            data = data.sort_index(ascending=True)
            data.to_csv(st_name)
        
        logger.debug(st_name + " Updated")
    
    logger.info("get_k_data Finished")

def get_k_list(refresh = True):
    ts_list = ts.get_stock_basics()
    if (refresh == True):ts_list.to_csv(g_data_path+'stock_list.cvs')
    return ts_list.index

#the parameter mean is what date before a(num) days.
def k_date_now(a = None):
    now = datetime.datetime.now()
    if a != None: now = now - datetime.timedelta(eval(a))
    today = now.strftime("%Y-%m-%d")
    logger.debug("date is " + today)
    return today

#def date_zone(start, end):

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
 
    isExists=os.path.exists(path)
 
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def get_tick_data(code = None, date = 'today'):
    date = k_date_now()
    for i in code:
        path = g_data_path + "tick/" + "i"
        mkdir(path)
        st_name = path + "/" + date
        if os.path.exists(st_name):
            continue

        df = ts.get_today_ticks(i) if date == 'today' else ts.get_tick_data(i, date)
        df.to_csv(st_name)

def format_data_1(arrays, index = None, columns = None):
    data = zip(*[iter(arrays)]*len(columns))
    df = pd.DataFrame(data, index=index, columns=columns)
    try:
        if df.empty:
            logger.debug("Error: did not get the format data")
            return ''
    except:
        return ''
    return df

def data_save(filepath, data):
    data.to_csv(filepath)

