# -*- coding: utf-8 -*-
import pandas as pd
import sys

comp_data = {}

for i in sys.argv[1:]:
    print i
    comp_data[i] = pd.read_csv(i).close_rate.mean()
    print comp_data[i]

print("The list include")

func = lambda d:d[1].close_rate.mean

rests = sorted(comp_data.iteritems(), key=lambda d:d[1], reverse=True)
print rests

def sort_pd(pds, col, ascend = False):
    sort_result = {}
    data = pd.DataFrame()
    for pd in pds:
        pd['rank'] = pd[col].rank(method="max", ascending=ascend)
        data['rank'] = data['rank'] + pd['rank']

    return data.sort_values(by='rank')


"""
def sort_combo(pds, cols):
    data = pd.DataFrame()

    for i in cols:
        sortd = sort_pd(pds, i['col'], i['ascend'])
        sortd

def sort_pds_ticks():

def sort_pds_class():
"""
