import os
import datetime
import time
import pandas as pd
import logging

g_data_path = './data/'
g_log_path = './'
logger = logging.getLogger('slogger')

#init log system and parameter
def init():
    fh = logging.FileHandler(g_log_path + 'test.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info("Init finished")


def refresh_k_data(code_list, k = None):
    logger.info("get_k_data start...")
    today = k_date_now()
    for code in code_list:
        st_name = filename + code + '.csv'
        
        logger.debug("path is " + st_name)
        data = None
        
        if os.path.exists(st_name):
            csv_data = pd.read_csv(st_name)
            csv_latest = csv_data.date
            csv_latest = csv_latest.iloc[-1]
        
            if csv_latest == today:
                logger.debug(st_name + " have alrealy")
                continue
        
            logger.debug(csv_latest + " -- " + today)

            data = ts.get_k_data(code, start = csv_latest, end = today ) if (k) else ts.get_hist_data(code, start = csv_latest, end = today )
            try:
                if data.empty or data.shape[0] < 2:
                    logger.debug("Error: did not get the data")
                    continue
            except:
                continue
            
            data = data.sort_index(ascending=True)
            data = data.drop(data.index[0])
            data.to_csv(st_name, mode = 'a', header=None)
        
        else:

            data = ts.get_k_data(code) if (k) else ts.get_hist_data(code)
            try:
                if data.empty:
                    logger.debug("Error: did not get the data")
                    continue
            except:
                continue
        
            data = data.sort_index(ascending=True)
            data.to_csv(st_name)
        
        logger.debug(st_name + " Updated")
    
    logger.info("get_k_data Finished")


def get_k_list(refresh = True):
    ts_list = ts.get_stock_basics()
    ts_list.to_csv(filename+'stock_list.cvs' if (refresh)
    return ts_list.index

def k_date_now(a = None):
    now = datetime.datetime.now()
    if a != None: now = now + datetime.timedelta(eval(a))
    today = now.strftime("%Y-%m-%d")
    logger.debug("date is " + today)
    return today


def 



