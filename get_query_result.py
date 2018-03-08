# coding:utf-8
import requests
import random
import pymysql
from lxml import etree
from header_list import user_agent
from get_proxies import get_proxies_with_limit


def get_city_name(num,proxy_dict):
    url='http://www.ip138.com:8080/search.asp?mobile='+str(num)+'&action=mobile'
    #print (url)
    rand_index=random.randint(0,7)
    agent=user_agent[rand_index]
    headers={'user-agent':agent}
    #print headers
    proxies=proxy_dict
    #print(proxy_dict)
    result=requests.get(url,headers,proxies=proxies)
    web_page=bytes(result.text,'iso-8859-1')
    processed_page=web_page.decode('gb2312')
    soure=etree.HTML(processed_page)
    city=soure.xpath('//tr[@class="tdc"]/td[@class="tdc2"]/text()')
    city_name="".join(city[1].split())
    phone_num_type=soure.xpath('//tr[@class="tdc"][3]/td[@class="tdc2"]/text()')
    return city_name,phone_num_type[0]


def get_proxy(proxies_list):
    proxy=proxies_list[0]
    proxy_info=proxy.split('|+|')
    if proxy_info[1]=='HTTP':
        proxy_str='http://'+proxy_info[0]
        proxy_dict={'http':proxy_str}
    else:
        proxy_str='https://'+proxy_info[0]
        proxy_dict={'https':proxy_str}
    return proxy_dict


def delete_proxy(proxy,proxies_list):
    proxies_list.remove(proxy)


def create_conn(host,user_name,password,db_name):
    conn = pymysql.connect(host, user_name, password, db_name,charset='utf8')
    return conn


def save_query_result(phone_num_prefix,city_name,phone_num_type,conn):
    sql_str='INSERT INTO phone_num_info VALUES ({num},\'{city_name}\',\'{num_type}\');'\
        .format(num=phone_num_prefix,city_name=city_name,num_type=phone_num_type)
    print(sql_str)
    cursor=conn.cursor()
    cursor.execute(sql_str)
    conn.commit()


def save_break_position(break_position):
    with open('position.txt','w') as f:
        f.writelines(break_position)
if __name__== '__main__':
    conn=create_conn('localhost','root','666666','test')
    proxies_list=get_proxies_with_limit(1)
    phone_num_prefix=1300000
    while phone_num_prefix<1400000:
        try:
            proxy=get_proxy(proxies_list)
            city_name,phone_num_type=get_city_name(phone_num_prefix,proxy)
            save_query_result(phone_num_prefix,city_name,phone_num_type,cursor)
            phone_num_prefix+=1
        except requests.exceptions.ProxyError:
            delete_proxy(proxies_list[0],proxies_list)
        except Exception as e:
            save_break_position(phone_num_prefix)
            print('Unexpected Error: {}'.format(e))


