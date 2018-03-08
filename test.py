# coding:utf-8
import pymysql


def create_conn(host,user_name,password,db_name):
    conn = pymysql.connect(host=host, user=user_name, password=password, database=db_name,charset='utf8')
    return conn


def save_query_result(phone_num_prefix,city_name,phone_num_type,conn):
    sql_str='INSERT INTO phone_num_info VALUES ({num},\'{city_name}\',\'{num_type}\');'\
        .format(num=phone_num_prefix,city_name=city_name,num_type=phone_num_type)
    print(sql_str)
    cursor=conn.cursor()
    cursor.execute(sql_str)
    conn.commit()


if __name__=='__main__':
    conn= create_conn('localhost', 'root', '666666', 'test')
    save_query_result('1369602','四川南充','中国移动',conn)