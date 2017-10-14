# -*- coding: utf-8 -*-
import scrapy
from scrapy import WebScrapy
import basics
from basics import *
import re

"""
colm:   code: 代码
        p_change: 涨幅
        cprice: 收盘价
        price: 成交均价
        zyl:折溢率
        tvol:成交量
        tval:成交额
        cjeltszb: 成交额流通市值
        BUYERNAME: 买方营业部
        SALESNAME: 卖方营业部
        RCHANGE1DC: 1日涨幅(上榜后)
        RCHANGE5DC: 5
        RCHANGE10DC: 10
        RCHANGE20DC: 20
"""

_token_url = 'http://data.eastmoney.com/dzjy/detail/<CODE>.html'
_token_reg = 'em_mutisvcexpandinterface.*token=(\d|\w+)\&'
_url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?token=<TOKEN>&cmd=&st=TDATE&sr=-1&p=1&ps=<NUMBER>&filter=(SECUCODE=%27<CODE>%27)&js=var%20UObvwgvJ={pages:(tp),data:(x)}&type=DZJYXQ&rt=50253591'
_data_reg = 'data\:\[(.+)\]'
_date_reg = 'filter=\(SECUCODE=.*\)\&'

#大单 of eastmoney.com 
class EMDDScrapy(WebScrapy):
    def __init__(self, name = 'Dadan', token_url = None, token_reg = None, url = None, colm=None, index = None):
    #["code", "p_change", "cprice", "price", "zyl", "tvol", "tval", "cjeltszb", "BUYERNAME", "SALESNAME", "RCHANGE1DC", "RCHANGE5DC", "RCHANGE10DC", "RCHANGE20DC"], index = None):
        self.name = name
        self.types = "MU"
        self.token_url = token_url if token_url != None else _token_url
        self.token_reg = token_reg if token_reg != None else _token_reg
        self.url = url if url != None else _url
        self.colm = colm
        self.index = index

        basics.mkdir(g_data_path + '/' + self.name)
        WebScrapy.__init__(self, self.name, self.token_url, self.token_reg, self.url, self.types, self.colm, self.index)
        
        url = re.sub('\<CODE\>', '600600', self.token_url)
        text = self.get_html_text(url)
        if text == '': return False
        self.token_string = self.get_token()

    def get_data(self, text):
        data = re.findall(_data_reg, text)
        
        try:
            data = '[' + data[0] + ']'
            data_array = eval(data)
            return data_array
        except:
            return False

    def refresh(self, code, number):
        url = re.sub('\<CODE\>', code, self.token_url)
        
        data_url = re.sub('\<TOKEN\>', self.token_string, self.url)
        data_url = re.sub('\<CODE\>', code, data_url) if code.isdigit() else re.sub(_date_reg, '', data_url)
        number = '%d' % number
        data_url = re.sub('\<NUMBER\>', number, data_url)

        data_text = self.get_html_text(data_url)
        data_array = self.get_data(data_text)
        
        data = basics.format_hash_pd(data_array)
        return data
        #data.to_csv(self.file_path_csv(code))

    def refresh_latest_dd(self, date = 0, number = 50):
        date = date + 1
        data = self.refresh('', number)
        date = k_date_now(date)
        ##重新刷新时间格式
        data = data.replace('T00\:00\:00', '', regex=True)
        data = data[data.TDATE >= date]
        data.to_csv(self.file_path_csv(date))
       
        return data

    def refresh_st_dd(self, code, number = 50):
        logger.info("try to get dd of %s" % (code))
        try:
            data = self.refresh(code, number)
            data.to_csv(self.file_path_csv(code))
        except:
            logger.debug("ERROR: refresh dd of %s" % (code))
"""
    def refresh_sk_today(self):
        logger.info("try to refresh dd of today")
        data = self.refresh_latest_dd(number = 500)
        
        for i in 
        data.to_csv(st_name, mode = 'a', header=None)
   """     