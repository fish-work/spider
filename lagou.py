def Get_url(key_word,city,salary_range):
    """
    函数作用：按参数生成需要爬去拉勾的url和referer_url
    
    :param key_word: 职位关键字：例如：python
    :param city: 意向城市：例如：北京
    :param salary_range: 薪资水平（请详见下方salary dict）（该字段是可选的，默认不限）：例如：1表示<2k/M,6表示25k-50k/M
    :return:返回需要向拉勾请求的url地址和重定向的地址
    """
    salary = {1:'2k',
              2:'2k-5k',
              3:'5k-10k',
              4:'10k-15k',
              5:'15k-25k',
              6:'25k-50k',
              7:'50k' }
     
    if salary_range is not None:
        url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&yx=' + salary[salary_range] + '&city=' + city
    else:
        url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=' + city
        
    referer_url = 'https://www.lagou.com/jobs/list_' + key_word + '?px=default&city=' + city

    return url,referer_url

def Read_url(key_word,city,number,salary_range):
    """
    函数作用：读取需要爬去的url内容，返回结果
    
    :param key_word: 职位关键字：例如：python
    :param city: 意向城市：例如：北京
    :param number: page_number，页数，第几页，从1开始
    :param salary_range: 薪资水平（请详见下方salary dict）（该字段是可选的，默认不限）：例如：1表示<2k/M,6表示25k-50k/M
    :return:返回拉勾返回的json文件
    """
    from urllib2 import Request,urlopen
    import urllib
    
    url,referer_url = Get_url(key_word,city,salary_range)
    
    headers = {
    'Referer':referer_url,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}
    
    values = {'first' : 'false',  
          'pn' : number,  
          'kd' : key_word } 
    
    req_data = urllib.urlencode(values)
    
    req = Request(url,req_data,headers)
    data = urlopen(req).read()
    
    return data
    
def Deal_data(data):
    """
    函数作用：对获取的url返回结果进行处理
    
    :param data: 返回拉勾返回的json文件
    :return:对拉勾返回的json文件进行处理，处理成dataframe格式
    """
    data_json = json.loads(data)
    #try:
    #    target_data = data_json['content']['positionResult']['result']
    #except:
    #    print data_json
    if 'content' in data_json.keys():
        target_data = data_json['content']['positionResult']['result']
        df = pd.DataFrame(target_data)
    
        columns = ['companyFullName','companyShortName','secondType','city','businessZones','positionName','positionLables','salary','workYear','positionAdvantage','companyLabelList']
    
        df = df[columns]
    else:
        df = pd.DataFrame()
    return df

def Get_url_info(key_word,city,number,salary_range):
    """
    函数作用：关键函数，对符合参数的指定页的内容，进行读取，处理，并返回结果
    
    :param key_word: 职位关键字：例如：python
    :param city: 意向城市：例如：北京
    :param number: page_number，页数，第几页，从1开始
    :param salary_range: 薪资水平（请详见下方salary dict）（该字段是可选的，默认不限）：例如：1表示<2k/M,6表示25k-50k/M
    :return:返回拉勾返回的json文件处理后的目标数据
    """
    data = Read_url(key_word,city,number,salary_range)
    
    df = Deal_data(data)
    
    return df

def LaGou(key_word,city,salary_range = None):
    """
    函数作用：主函数，按页获取数据并处理，然后合并返回结果
    
    :param key_word: 职位关键字：例如：python
    :param city: 意向城市：例如：北京
    :param salary_range: 薪资水平（请详见下方salary dict）（该字段是可选的，默认不限）：例如：1表示<2k/M,6表示25k-50k/M
    :return:返回拉勾返回的所有页面的json文件处理后的目标数据
    """
    from urllib2 import Request,urlopen
    import pandas as pd
    import time
       
    df = pd.DataFrame()
    
    number = 1
    Flag = True
    while Flag:
        print 'number:',number
        mid_df = Get_url_info(key_word,city,number,salary_range)
        time.sleep(5)
        if mid_df.empty:
            Flag = False
        else:
            df = pd.concat([df,mid_df])
            number += 1
    
    return df

if __name__ == '__main__':
    key_word = 'c++'
    city = '北京'
    salary_range = 6
    
    df = LaGou(key_word,city,salary_range)
    print df
