import traceback
from kafka.errors import kafka_errors
import baostock as bs
import Utils


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

    #### 登出系统 ####
    bs.logout()

    #返回股票数据
    # return data_list
    print(data_list)

def main():
    conf=func.get_config()

    producer=func.get_kafka_producer(conf)

    count = 0

    for info in get_stock_info():
        count += 1
        future = producer.send(
            'test',
            key=f'{count}',  # 同一个key值，会被送至同一个分区
            value='{' + f'data:{info}' + '}',
            partition=0)
        try:
            future.get(timeout=10)  # 监控是否发送成功
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()

    producer.close()

if __name__ == '__main__':
    main()