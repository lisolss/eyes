# -*- coding: utf-8 -*-
import em_scrapy
from em_scrapy import EMMFScrapy
import basics
import scrapy
from basics import *
from k import KAs
import sys
from ticks import TKAs
from dd_scrapy import EMDDScrapy
import tradeday

class EyesReporter:
    def __init__(self, type):
        self.type = type
        self.cs = 2
        self.path = g_data_path + "/ticks/"
        self.dd = TKAs()
    
    #exec
    def data_require(self, requires):
        pass


    def data_output_format(self, output):
        pass
    
    """
    def _get_x_data(self):
    
    def _get_y_data(self):
    """ 

    def _time_zone(self, type, val = 1, tzone = 'd'):
        pass

    #基础的report函数, 输出是时间, 类型和vaile的列表. type是分析的类型, 比如成交量, 成交次数一类的.
    #
    #
    def _class_report(self, type, val = 'all', tzone = 'd', top = 0):
        t_file_list = os.listdir(self.path)
        
        report_data = pd.DataFrame([], columns=['date', 'class_name', 'value'])
        for t in t_file_list:
            _tpath = self.path + t
            _class_data = pd.read_csv(_tpath+'/summary_classified.csv')
            _class_data = _class_data.loc[:,['c_name', type]]
            _class_data['date'] = t
            _class_data = _class_data.rename(columns={'c_name':'class_name', type:'value'})

            if top != 0:
                _class_data = _class_data.sort_values(['value'])[:top]
           
            report_data = report_data.append(_class_data, ignore_index=True)
            
        return report_data

    def _ticks_report(self, type, list, tzone):
        self._update_data(tzone)
        
        t_file_list = os.listdir(self.path)

        report_data = pd.DataFrame([], columns=['date', 'class_name', 'value'])
        for t in t_file_list:
            _tpath = self.path + t
            _class_data = pd.read_csv(_tpath+'/summary_classified.csv')
            _class_data = _class_data.loc[:,['c_name', type]]
            _class_data['date'] = t
            _class_data = _class_data.rename(columns={'c_name':'class_name', type:'value'})
           
            report_data = report_data.append(_class_data, ignore_index=True)
            
        return report_data


    #Update ticks detail if have not in disk
    def _update_data(self, datea, type = 'k'):
        start_time = end_time = ''
        if datea.find('-') != -i:
            start_time = datetime.datetime.strptime(datea.split('-')[0], '%Y%m%d')
            end_time = datetime.datetime.strptime(datea.split('-')[1], '%Y%m%d')
        else:
            start_time = datetime.datetime.strptime(datea, '%Y%m%d')
            end_time = datetime.datetime.strptime(datea, '%Y%m%d')
        
        date_list = tradeday.get_tradeday_list(start_time, end_time)
        for i in date_list:
            self.dd.refresh_all_ticks(i)
    

    


"""
a = EyesReporter('test')

#print a._class_report('buy_count')
v = a._class_report('buy_count')

_x_time = v['date'].drop_duplicates()

_x_time = _x_time.values
_point = v['class_name'].drop_duplicates().values
#print v[v.class_name == 'hs300']
for i in _point:
    print type(v[v.class_name == i])
    _value = v[v.class_name == i].sort_values(['date'])
    print _value
    _val = _value['value'].values
    print _val
    #line.add(i, _x_time, _val)
    
#print line
"""