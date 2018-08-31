import requests
import datetime  
'''  
@query a single date: string '20170401';  
@api return day_type: 0 workday 1 weekend 2 holiday -1 err  
@function return day_type: 1 workday 0 weekend&holiday  
'''  
  
  
def get_day_type(query_date):  
    url = 'http://tool.bitefu.net/jiari/?d=' + query_date  
    resp = requests.get(url)  
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    content = resp.text 

    if content:  
        try:  
            day_type = int(content)  
        except ValueError:  
            return -1  
        else:  
            return day_type  
    else:  
        return -1  
  
  
def is_tradeday(query_date):  
    weekday = datetime.datetime.strptime(query_date, '%Y%m%d').isoweekday()  
    if weekday <= 5 and get_day_type(query_date) == 0:  
        return 1  
    else:  
        return 0  
  
def today_is_tradeday():  
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')  
    return is_tradeday(query_date)  

def get_latest_tradeday(date):
    #date = datetime.datetime.strptime(date, '%Y%m%d')

    yesterday = date - datetime.timedelta(days=1)

    while(1):
        if is_tradeday(yesterday.strftime('%Y%m%d')) == 1:
            break
        yesterday = yesterday - datetime.timedelta(days=1)

    return yesterday

def get_tradeday_list(start_time, end_time):
    date_list = []

    while(1):
        if os.path.isdir(self.path + day.strftime('%Y%m%d')) == True: 
            continue
        else:
            if is_tradeday(start_time.strftime('%Y%m%d')) == 1:
                date_list.append(start_time.strftime("%Y%m%d"))

        if (end_time - start_time).days == 0:
            break

        start_time =  start_time + datetime.timedelta(1)
    
    return date_list

