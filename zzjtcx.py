def Get_cookie(url):
    """
    save url的cookie
    """
    
    file_name = 'D:\\cookie.txt'
    
    cookie = cookielib.MozillaCookieJar(file_name) 
    #声明一个CookieJar对象实例来保存cookie
    handle = urllib2.HTTPCookieProcessor(cookie)
    #通过handle来构建opener
    opener = urllib2.build_opener(handle)
    #此open方法与urllib2的urlopen方法，可以传入request
    response = opener.open(url) 
    cookie.save(ignore_discard=True,ignore_expires=True)

def Read_url(url_common,file):
    """
    获取 url的返回的数据
    """
    header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Referer':url_common
    #'Referer':'http://www.zzjtcx.com/'
}
    #url_file = 'http://www.zzjtcx.com/sy/gjds/getCongestionRoad.htm'
    
    url_file = url_common + '/' + file
    
    
    #
    cookie = cookielib.MozillaCookieJar()
    #
    cookie.load('D:\\cookie.txt',ignore_discard=True,ignore_expires=True)
    
    req = Request(url_file,None,headers=header)
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
    data = opener.open(req).read()
    
    return data

def Deal_data(data):
    """
    处理 url的返回的数据
    """
    data_list = data[1:-1].split('},')
    df = pd.DataFrame()
    for num,data_detail in enumerate(data_list):
        if num == len(data_list) - 1:
            pass
        else:
            data_detail += '}'
        json_data = json.loads(data_detail)
        mid_df = pd.DataFrame([json_data.values()],columns = json_data.keys())
        df = pd.concat([df,mid_df])
    return df
 
def zzjtcx():
    """
    主程序
    """
    Host = 'http://www.zzjtcx.com'
    Host_file = '/sy/gjds/getCongestionRoad.htm'

    #save cookie
    Get_cookie(Host)
    
    url_data = Read_url(Host,Host_file)
    
    df = Deal_data(url_data)
    
    return df
   
   if __name__ == '__main__':
    import cookielib
    import urllib2
    from urllib2 import Request,urlopen
    import pandas as pd
    import json

    df = zzjtcx()
    print df
