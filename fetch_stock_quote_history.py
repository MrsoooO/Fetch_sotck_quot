import re
import threading

import pymysql
from dbutils import persistent_db
import Properties
import baostock as bs

def __inint__(prop):
    conn=persistent_db.connect(creator=pymysql
                               ,host=prop['host']
                               ,user=prop['user']
                               ,passwd=prop['passwd']
                               ,port=int(prop['port'])
                               ,db=prop['db'])
    return conn

def get_stock_relation(conn,date):
    lg = bs.login()
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    rs = bs.query_all_stock(day=date)
    print('query_all_stock respond error_code:' + rs.error_code)
    print('query_all_stock respond  error_msg:' + rs.error_msg)
    data_list=[]
    count=0
    while (rs.error_code=='0') & rs.next():
        data_list.append(rs.get_row_data())
    # 若有自增主键需要锁
    # lock = threading.Lock()
    for row in data_list:
        # lock.acquire()
        sql = 'insert into stock.stock_relation values(' + '\'' +str(row[0].split('.')[1]) + '\'' + ',' + '\'' +row[2] +\
              '\'' + ',' + '\'' + row[0].split('.')[0] + '\'' + ',' + '\'' + str(row[1]) + '\'' + ')'
        # print(sql)
        cur=conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            count+=1
            r=cur.fetchone()
            # print(r)
        except Exception as e :
            conn.rollback()
            raise e
        finally:
            sql=''
            cur.close()
            conn.close()
            # lock.release()
    print('数据同步完成,总共同步' + str(count) + '条数据')

def get_stock_quote_history(conn,start=None,end=None,period="d",adjust="3"):
    stock_list=[]
    cur=conn.cursor()
    cur.execute("select concat(market_code,'.',stock_code) from stock.stock_relation")
    result=cur.fetchall()
    for i in result:
        stock_list.append(i[0])
    target_list = []
    cur.execute("select concat(market_code,',',stock_code) from stock.stock_quote_history group by stock_code ,market_code")
    result=cur.fetchall()
    for i in result:
        target_list.append(i[0])
    final_list = list(set(stock_list) - set(target_list))
    # print(stock_list)
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    count=1
    for code in final_list:
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date=start, end_date=end,
                                          frequency=period, adjustflag=adjust)
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
        # print(quote_list)
        if rs.error_code != '0':
            pass
        else:
            quote_list = []
            while (rs.error_code == '0') & rs.next():
                quote_list.append(rs.get_row_data())
            sql = 'insert into stock.stock_quote_history values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql_list = []
            for quote in quote_list:
                sql_list.append((quote[0],quote[1].split('.')[1],quote[1].split('.')[0],quote[2],quote[3],quote[4],quote[5],quote[6],quote[7],quote[8],
                                 quote[9],quote[10],quote[11],quote[12],quote[13],quote[0].split('-')[0]))
                # print(sql_list)
            cur=conn.cursor()
            try:
                cur.executemany(sql,sql_list)
                conn.commit()
                count += 1
                print('已同步' + str(count) + '支股票')
            except Exception as e :
                print(e)
                conn.rollback()
            finally:
                cur.close()
                conn.close()
                quote_list = []

    bs.logout()
    print("已同步" + str(count) + "支股票历史数据")

def main():
    # get_stock_relation(__inint__(Properties.getProp('info.properties')),'2023-01-06')
    get_stock_quote_history(__inint__(Properties.getProp('info.properties')))

if __name__ == '__main__':
    main()