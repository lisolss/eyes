# -*- coding: utf-8 -*-
import scrapy
from scrapy import WebScrapy
import basics
import re
#机构调研
"""
colm:   market:sh or sz
        SCode: 代码
        CompanyName: 
        NoticeDate: 公告日期
        StartDate: 调查日期
        Description: 描述
"""
_url_summary = 'http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=1000&page=1&js=var%20VSCyngEq&param=&sortRule=-1&sortType=0&rt=50282153'
_url_detail = 'http://view-source:http://data.eastmoney.com/jgdy/dyxx/<CODE>,<DATE>.html'

class EMJGDYScrapy(WebScrapy):
    def __init__(self, name = 'JGDY', url = None, colm=None, index = None):
    #["code", "p_change", "cprice", "price", "zyl", "tvol", "tval", "cjeltszb", "BUYERNAME", "SALESNAME", "RCHANGE1DC", "RCHANGE5DC", "RCHANGE10DC", "RCHANGE20DC"], index = None):
        self.name = name
        self.types = "MU"
        self.token_url = ''
        self.token_reg = ''
        self.url = url if url != None else _url
        self.colm = colm
        self.index = index

        basics.mkdir(g_data_path + '/' + self.name)
        WebScrapy.__init__(self, self.name, self.token_url, self.token_reg, self.url, self.types, self.colm, self.index)

    def get_data(self, text):
        data = re.findall(_data_reg, text)
        
        try:
            data = '[' + data[0] + ']'
            data_array = eval(data)
            return data_array
        except:
            return False

    def get_summary(self, timezone = 0):
        date = k_date_now(date, timezone)
        data_text = self.get_html_text(data_url)
        data_array = self.get_data(data_text)
        data = basics.format_hash_pd(data_array)
        data = data[data.StartDate == date]
        return data

    def get_detail():

    def get_who_history(self, who):