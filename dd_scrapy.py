# -*- coding: utf-8 -*-
import scrapy
from scrapy import WebScrapy
import basics
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

#大单 of eastmoney.com 
class EMDDScrapy(WebScrapy):
    def __init__(self, token_url, token_reg, url, colm=["code", "p_change", "cprice", "price", "zyl", "tvol", "tval", "cjeltszb", "BUYERNAME", "SALESNAME", "RCHANGE1DC", "RCHANGE5DC", "RCHANGE10DC", "RCHANGE20DC"], index = None):
        self.name = "DaDan"
        self.types = "MU"
        self.token_url = token_url
        self.token_reg = token_reg
        self.url = url
        self.colm = colm
        self.index = index
        WebScrapy.__init__(self, self.name, token_url, token_reg, url, self.types, colm, index)

    def get_data(self, text, regs='([\d\:\-\.]+),'):
        data = re.findall('data\:\[(.+)\]', text)
        
        try:
            data = '[' + data[0] + ']'
            data_array = eval(data)
            return data_array
        except:
            return False
        

    def do(self):
        text = self.get_html_text(self.token_url)
        if text == '': return False

        token_string = self.get_token()

        data_url = re.sub('\<TOKEN\>', token_string, self.url)
        print data_url
        data_text = self.get_html_text(data_url)
        data_array = self.get_data(data_text)
        data = basics.format_data_1(data_array, self.index, self.colm)
        print self.file_path_csv()
        data.to_csv(self.file_path_csv()) 