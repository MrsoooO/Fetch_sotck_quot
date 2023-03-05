import traceback
import requests
import threading
import json
import time
import dbutils.persistent_db
import pymysql

def __init__():
    pool = dbutils.persistent_db.PersistentDB(creator=pymysql
                                            ,host='localhost'
                                            ,user='root'
                                            ,passwd='123321Xu'
                                            ,db='stock'
                                            ,port=3306)
    conn = pool.connection()
    return conn


def spyder(conn):

    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}

    prefix= 'http://9.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124035564170271449824_1677938925169&pn='

    suffix= '&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1677938925170'

    flag=True

    pagenum = 1

    lock=threading.Lock()

    while flag:

        url=prefix + str(pagenum) + suffix

        rq=requests.get(url,headers)

        js=json.loads(rq.text.split('(')[1].split(')')[0])

        if js['data'] == None:
            flag=False
        else:
            data_list=js['data']['diff']
            lock.acquire()
            try:
                for data in data_list:
                    sql = 'insert into stock_quote(stock_code,stock_name,current_price,open_price,max_price,min_price,last_day_price,limits,wave,' \
                          'volumn,turnover,turnover_rate,earning_dynamic,earning_static,busi_date,years)values('

                    if isinstance(data['f3'],str) or isinstance(data['f7'],str) :
                        # sql = sql + str(data['f12'])
                        sql = 'insert into stock_quote(stock_code ,stock_name , busi_date ,years) values( ' + str(data['f12']) + ',' +'\''+ str(data['f14']) + '\'' + \
                              ',' + '\''+ str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))+'\'' + ',' + str(time.strftime('%Y',time.localtime())) + ')'
                    else:
                        sql= sql +'\'' + str(data['f12']) + '\'' + ',' +'\'' +str(data['f14'])+'\'' + ',' + str(data['f2']) + ',' + str(data['f17']) + ',' \
                             + str(data['f15']) + ',' + str(data['f16']) + ',' + str(data['f18']) + ',' + str(data['f3']/100) + ',' \
                             + str(data['f7']/100) + ',' + str(data['f5']) + ',' + str(data['f6']) + ',' + str(data['f8']) + ',' \
                             + str(data['f9']) + ',' + str(data['f22']) + ',' +'\''+ str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))+'\'' \
                             + ',' + str(time.strftime('%Y',time.localtime())) + ')'
                        # print(sql)

                    cur=conn.cursor()
                    try:
                        cur.execute(sql)
                        conn.commit()
                    except pymysql.Error as e:
                        print(e.args[0],e.args[1])
                        traceback.print_exc()

                    cur.close()
                    conn.close()
            finally:
                lock.release()
        pagenum += 1

def main():
    conn=__init__()
    spyder(conn)


if __name__ == '__main__':
    main()