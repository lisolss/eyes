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