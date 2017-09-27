import requests
from bs4 import BeautifulSoup
import traceback
import re
import pandas as pd

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
"""
tx = getHTMLText("http://data.eastmoney.com/zjlx/detail.html")

pattern = re.compile('dataurl.*token=(\d|\w+)\{')
res = re.search(pattern, tx)
print res.group(1)
"""

def format_data(arrays, indexs = None, columnss = None):
    data = zip(*[iter(arrays)]*len(columnss))
    df = pd.DataFrame(data, index=indexs, columns=columnss)
    try:
        if df.empty:
            print("Error: did not get the format data")
            return ''
    except:
        return ''
    print df

#dd = format_data([1, 2, 3, 4, 5, 6, 7, 8], indexs = list("xy"),columnss = list("abcd"))
#print dd

class WebScrapy:

    def __init__(self, name, **age):
        self.name = name
        for key in age.keys():
            exec("self.%s = \'%s\'" % (key, age[key]))

        print self.test
        print self.test2

k = {'test':'ooo', 'test2':'o\d\p...oo2'}
a = WebScrapy("test", **k)
print "done"