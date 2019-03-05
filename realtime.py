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
import winsound
import thread 


from pytdx.errors import TdxConnectionError, TdxFunctionCallError
from pytdx.hq import TdxHq_API, TDXParams
from pytdx.exhq import TdxExHq_API

datas = []
config = {'speed_timeing':4, 'refresh':3, 'speed_gap':1}

def refresh_ticks_tdx(codes):
    date = datetime.datetime.now().strftime("%Y%m%d")
    api = TdxHq_API()
    api.connect(ip='125.64.41.12')
    
    while True:
        for i in range(len(codes)):
            
            index = 0
            for i2 in range(1000):
                last_als = codes[i][4].iloc[-1].time if len(codes[i][4]) != 0 else datetime.datetime.strptime("08:01", "%H:%M").strftime("%H:%M")
                data = api.to_df(api.get_transaction_data(codes[i][0], codes[i][1], index, 500))
                
                data = data[data.time >= last_als]
                if len(data) <= 0:
                    break

                if len(data) <= 499:
                    codes[i][2] = codes[i][2][~(codes[i][2].time == last_als)] #delete the old data because got same data again
                    codes[i][2] = pd.concat([data, codes[i][2]])
                    break
                else:
                    codes[i][2] = pd.concat([data, codes[i][2]])
                    index = index + 500
        

        als_data = _tr_als(codes, config['refresh']) ####timeline 却接口
        _display_als(als_data)
        time.sleep(5)
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        

###
#Data structure:
#time: 9:00 + timeline
#
###
def _tr_als(codes, timelines = 5):

    ticks = {}
    for i in range(len(codes)):
        last_als = codes[i][4].iloc[-1].time if len(codes[i][4]) != 0 else datetime.datetime.strptime("09:10", "%H:%M").strftime("%H:%M")
                
        dfs = codes[i][2][codes[i][2].time >= last_als]
        if len(dfs) <= 0:    
            break

        for l in range(10000):
            timeline = datetime.datetime.strptime(last_als, "%H:%M") + datetime.timedelta(minutes=timelines)
            timeline = timeline.strftime("%H:%M")
            
            if (timeline > "11:30") and (timeline < "13:30"):
                last_als = timeline
                continue

            all_bs = dfs[dfs.time >= last_als]
            bs =  all_bs[all_bs.time < timeline]

            if len(bs) <= 0:
                if len(all_bs) <= 0:
                    break
                else:
                    last_als = timeline
                    df = format_data_1([last_als, 0, 0], columns=['time', 'bs_vol', 'bs_p'])
                    codes[i][4] = codes[i][4].append(df)
                    continue

            bs_vol = bs[bs.buyorsell == 0]['vol'].sum() -  bs[bs.buyorsell == 1]['vol'].sum()
            
            bs.insert(0, 'p', bs['price'].mul(bs['vol'])*100)

            bs_p = bs[bs.buyorsell==0]['p'].sum() - bs[bs.buyorsell == 1]['p'].sum()
            
            last_als = timeline
            df = format_data_1([last_als, bs_vol, bs_p], columns=['time', 'bs_vol', 'bs_p'])
            
            codes[i][4] = codes[i][4].append(df)

    return codes

def _display_als(als, counts=20):
    for i in range(len(als)):
        len_t = len(als[i][4])
        counts = counts if len_t >= counts else len_t
        clt = ""
        for l in range(counts):
            clt = clt + '+' if als[i][4].iloc[l-counts].bs_p > 0 else clt + '-'
        
        print("%s - %s - %s" % (als[i][1], als[i][4][(len_t-counts-1):len_t-1].bs_p.sum(), clt))


def _init_als_data(codes):
    datas = []
    for i in range(len(codes)):
        st = [0] * 5
        st[0] = codes[i][0]   #市场
        st[1] = codes[i][1]   #code
        st[2] = pd.DataFrame()#ticks data
        st[3] = 0             #index
        st[4] = pd.DataFrame(columns=['time', 'bs_vol', 'bs_p'])  #analyes result
        datas.append(st)

    return datas

def _risk_speed():
    timeing = config['speed_timeing'] * 60//config['refresh'] - 1
    
    if len(datas) <= timeing:
        return 0

    timeing = len(datas) - timeing
   
    for i in range(0, len(datas[-1])):
        speed = (datas[-1][i]['price'] - datas[timeing][i]['price'])/datas[timeing][i]['price']*100

        if abs(speed) > config['speed_gap']:
            print("%s speed is %f in the time!!!!!!!!!!!" %(datas[timeing][i]['code'], speed))
            if speed > 0:
                return -1
            return 1
    
    return 0


def risk():
    risks = _risk_speed()
    if risks > 0:
        print("RASK!!!")
        return 1
    
    if risks < 0:
        return -1
    return 0


def realtime(codes):
    api = TdxHq_API()
    api.connect(ip='125.64.41.12')
    failed = 0
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        data = api.get_security_quotes(codes)
        if data == None:
            time.sleep(1)
            failed = failed + 1
            if failed >= 10:
                api.connect(ip='114.80.63.71')
            continue
        
        failed = 0
        
        datas.append(data)
        message = risk()
        if message < 0:
            thread.start_new_thread(winsound.Beep, (200, 1000))
        elif message > 0:
            thread.start_new_thread(winsound.Beep, (600, 1000))
        
        for i in data:

            print("%s = %f = %f" %(i['code'],i['price'], (i['price']-i['last_close'])/i['last_close']*100))
        
        time.sleep(config['refresh'])
        
        print("\n\n")
    


thread.start_new_thread(winsound.Beep, (400, 5000))
codes = [(0, '000060'), (0, '000751'), (0, '001872'), (0, '002237'), (1, '600338'), (1, '600497'), (1, '600606'), (1, '603799')]
config = {'speed_timeing':3, 'refresh':3, 'speed_gap':1}

realtime(codes)

#datas = _init_als_data(codes)
#refresh_ticks_tdx(datas)
