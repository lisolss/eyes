# -*- coding: utf-8 -*-
import scrapy
from scrapy import WebScrapy
import basics
import re

"""
colm:   market:sh or sz
        code: 代码
        close: 最新价
        p_change: 涨幅
        main_: 主力单
        sl_: 超大单
        l_:大单
        m_:中单
        s_:小单
        _m: 量
        _r: 量比
"""

#money flow of eastmoney.com 
class EMMFScrapy(WebScrapy):
    def __init__(self, token_url, token_reg, url, colm=["market", "code", "close", "p_change", "mian_m", "mail_r", "sl_m", "sl_r", "l_m", "l_r", "m_m", "m_r", "s_m", "s_r"], index = None):
        self.name = "Money_Flow"
        self.types = "MU"
        self.token_url = token_url
        self.token_reg = token_reg
        self.url = url
        self.colm = colm
        self.index = index
        WebScrapy.__init__(self, self.name, token_url, token_reg, url, self.types, colm, index)

    def get_data(self, text, regs='([\d\:\-\.]+),'):
        data = re.findall(regs, text)
        try:
            data = data[1:]
        except:
                return False
        
        return data

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