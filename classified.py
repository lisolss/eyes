# -*- coding: utf-8 -*-
import basics
import pandas as pd
from k import KAs
import * form basics

class Classified():
    def __init__(self):
        self.st_name = g_data_path + '/classified/big_table.csv'
        self.big_table = pd.read_csv(self.st_name)

    #get classified data by code
    def get(self, code):
        if code.isdigit():
            return self.big_table(self.code == code).c_name
        else:
            return self.big_table(self.c_name == code).code

    def get_k(self, c_name):
        
        pass

    def get_vol(self, c_name):
        klist = self.get(c_name)
        start = basics.k_date_now(-100)
        end = basics.k_date_now()
        k = KAs(klist, start, end)
        
        vol = 0
        for code, data in k.data:
            vol = vol + data[0]

        pass

    def 
    