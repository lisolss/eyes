# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import traceback
import re
import basics
from basics import *

class WebScrapy:

    def __init__(self, name, token_url, token_reg, url, type, colm, index = None):
        self.name = name
        self.url = url
        self.reg_token = token_reg
        self.type = type
        self.colm = colm
        self.index = index
        self.logger = basics.logger
        self.logger.info("WebScarpy init finished with %s" % self.name)

    def get_html_text(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.latest_data = r.text
            return self.latest_data
        except:
            return ""

    #if reg_text have not data. it is will call latest data.
    def get_token(self, reg_text = None, reg_token = None):
        #if self.reg_token != '': self.reg_token = reg_token
        pattern = re.compile(reg_token) if reg_token != None else re.compile(self.reg_token)
        res = re.search(pattern, reg_text) if reg_text != None else re.search(pattern, self.latest_data)
        self.logger.info("The token is %s" %(res.group(1)))
        return res.group(1)

    def get_data_url(self, url, token):
        return re.sub('\<TOKEN\>', token, url)

    def file_path_csv(self, name = None):
        if name == None: 
            return '%s/%s/%s.csv' % (g_data_path, self.name, basics.k_date_now())
        else:
            return '%s/%s/%s.csv' % (g_data_path, self.name, name)
