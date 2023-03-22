# coding=utf-8
import baostock as bs
import numpy as np
import pandas as pd
import mplfinance as mpf
from inter_candles import InterCandle
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
    # return data_list
    # print(data_list)

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
def draw_k(df):
    # print(df)
    my_color = mpf.make_marketcolors(up='r',
                                     down='g',
                                     edge='inherit',
                                     wick='inherit',
                                     volume='inherit')
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                  figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
    normal_label_font = {'fontname': 'PingFang HK',
                         'size': '11',
                         'color': 'black',
                         'va': 'bottom',
                         'ha': 'right'}

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(['Date'], inplace=True)
    df=df.astype(float)
    # print(df)
    plot_data=df.iloc[100:200]
    last_data=plot_data.iloc[-1]
    fig=mpf.figure(style=my_style,figsize=(12,8),facecolor=(0.82,0.83,0.85))
    ax1=fig.add_axes([0.06, 0.25, 0.88, 0.60])
    ax2 = fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=ax1)
    ax3 = fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=ax1)
    ax1.set_ylabel('price')
    ax2.set_ylabel('volume')
    ax3.set_ylabel('macd')
    fig.text(0.50, 0.94, 'sh.600000:')
    fig.text(0.12, 0.89, 'Open/Close: ',**normal_label_font)
    fig.text(0.14, 0.89, f'{np.round(last_data["Open"], 3)} / {np.round(last_data["Close"], 3)}')
    fig.text(0.12, 0.86, f'{last_data.name.date()}')
    fig.text(0.40, 0.90, 'High: ',**normal_label_font)
    fig.text(0.40, 0.90, f'{last_data["High"]}')
    fig.text(0.40, 0.86, 'Low: ',**normal_label_font)
    fig.text(0.40, 0.86, f'{last_data["Low"]}')
    fig.text(0.55, 0.90, 'Volum(M): ',**normal_label_font)
    fig.text(0.55, 0.90, f'{np.round(last_data["Volume"] / 1000000, 3)}')

    mpf.plot(plot_data,
             ax=ax1,
             volume=ax2,
             type='candle',
             style=my_style)
    fig.show()
    # mpf.plot(plot_data,type='candle',ylabel='price',style=my_style,title='test',
    #          mav=(5,21),volume=True,figratio=(16,8),figscale=2,ylabel_lower='Volume',savefig=f'./{np.random.random(1)}.png')

def main():
    # producer=Kafka('./Config.ini').kafka_producer()
    #
    # producer.send('test',"asdasd")
    #
    # producer.close()
    my_color = mpf.make_marketcolors(up='r',
                                     down='g',
                                     edge='inherit',
                                     wick='inherit',
                                     volume='inherit')
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                  figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
    data=get_stock_data("sh.600000")
    df=data_processing(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(['Date'], inplace=True)
    df=df.astype(float)
    candle= InterCandle(df,my_style)
    candle.refresh_plot(150)
    # print(plt.get_backend())
    #https://blog.csdn.net/Shepherdppz/article/details/117575286
if __name__ == '__main__':
    main()