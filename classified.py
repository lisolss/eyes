# -*- coding: utf-8 -*-
import basics
import pandas as pd
import * form basics

class Classified():
    def __init__(self):
        self.st_name = g_data_path + '/classified/big_table.csv'
        self.big_table = pd.read_csv(self.st_name)

    #get classified data by code
    def gc(self, code):
        if code.isdigit():
            return self.big_table(self.code == code).c_name

        else:
            return self.big_table(self.c_name == code).code