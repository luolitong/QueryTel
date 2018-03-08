# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup

def get_proxies_with_limit(limit):
    add_list = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
                'AppleWebKit/537.36 (KHTML, like Gecko)' \
                ' Chrome/64.0.3282.186 Safari/537.36'
    headers = {'user-agent': user_agent}
    url = 'http://www.xicidaili.com/nn/'
    for num in range(limit):
        port_list = []
        ip_list=[]
        proxies_type_list=[]
        result = requests.get(url, headers=headers)
        soup=BeautifulSoup(result.text,'html.parser')
        # ip=soup.find_all('tr',class_='odd')
        ip_list=soup.find_all(text=re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'))
        port=soup.find_all('td',text=re.compile(r'^\d{2,5}?$'))
        proxies_type=soup.find_all('td',text=re.compile(r'^[[A-Z]{4,5}$'))
        for type in proxies_type:
            proxies_type_list.append(type.string)
        for each in port:
            port_list.append(each.string)
        for i in range(len(port_list)):
            add_list.append(ip_list[i]+':'+port_list[i]+'|+|'+proxies_type_list[i])
    #print(add_list)
    return add_list
# if __name__=='__main__':
#     get_proxies(2)