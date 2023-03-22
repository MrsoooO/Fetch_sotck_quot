# coding=utf-8
import baostock as bs
import numpy as np
import pandas as pd
import mplfinance as mpf
from Candle import DrawCandle
import matplotlib.pyplot as plt



def get_stock_info():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取证券基本资料
    rs = bs.query_stock_basic()
    print('query_stock_basic respond error_code:' + rs.error_code)
    print('query_stock_basic respond  error_msg:' + rs.error_msg)

    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    # 登出系统
    bs.logout()
    return data_list

def get_stock_data(stock_full_name,frequency='d',adjustflag='3',start_date='',end_date=''):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取沪深A股历史日K线数据 ####
    rs = bs.query_history_k_data_plus(stock_full_name,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=start_date, end_date=end_date,
                                      frequency=frequency, adjustflag=adjustflag)
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    data=pd.DataFrame(data_list,columns=rs.fields)
    #### 登出系统 ####
    bs.logout()

    #返回股票数据
    return data

def data_processing(data):
    df = data[['date','open','high','low','close','volume']]
    df.rename(columns={
        'date':'Date',
        'open':'Open',
        'high':'High',
        'low':'Low',
        'close':'Close',
        'volume':'Volume'
    },inplace=True)
    return df

def main():
    my_color = mpf.make_marketcolors(up='r',
                                     down='g',
                                     edge='inherit',
                                     wick='inherit',
                                     volume='inherit')
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                  figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
    # data=get_stock_data("sh.600000")
    # df=data_processing(data)
    # candle=DrawCandle(df,my_style)
    # candle.draw_plot()
    #https://blog.csdn.net/Shepherdppz/article/details/117575286
    data=get_stock_data("sh.600000")
    df=data_processing(data)
    # df['Date'] = pd.to_datetime(df['Date'])
    # df.set_index(['Date'], inplace=True)
    # df = df.astype(float)
    candle=DrawCandle(df,my_style)
    candle.draw_plot(20)
    # df1=df.loc[:,'Close'].to_frame()
    # df1['ma']=df1['Close'].rolling(window=20).mean()
    # df1['diff']=df1['Close'].rolling(window=20).std()
    # df1['upper']=df1.apply(lambda x : x['ma'] + 2 * x['diff'],axis=1)
    # print(df1)
    # print(boll)
if __name__ == '__main__':
    main()