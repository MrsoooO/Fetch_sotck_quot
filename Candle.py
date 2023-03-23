#encoding=utf-8
import mplfinance as mpf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
class DrawCandle:
    def __init__(self, data, my_style,start=-100,end=-1):
        self.data=data
        self.my_style=my_style
        self.start=start
        self.end=end
        self.last_data=data.iloc[self.end]
        # self.fig=mpf.figure(style=self.my_style,figsize=(12,8),facecolor=(0.82,0.83,0.85))
        # fig=self.fig
        # self.ax1=fig.add_axes([0.08, 0.25, 0.88, 0.60])
        # self.ax2=fig.add_axes([0.08, 0.15, 0.88, 0.10],sharex=self.ax1)
        # self.t1 = fig.text(0.50, 0.94, 'TITLE', )
        # self.t2 = fig.text(0.12, 0.90, '开/收: ', )
        # self.t3 = fig.text(0.14, 0.89, '',)
        # self.t4 = fig.text(0.14, 0.86, '',)
        # self.t5 = fig.text(0.22, 0.86, '', )
        # self.t6 = fig.text(0.12, 0.86, '',)
        # self.t7 = fig.text(0.40, 0.90, '高: ')
        # self.t8 = fig.text(0.40, 0.90, '')
        # self.t9 = fig.text(0.40, 0.86, '低: ')
        # self.t10 = fig.text(0.40, 0.86, '')
        # self.t11 = fig.text(0.55, 0.90, '量(万手): ')
        # self.t12 = fig.text(0.55, 0.90, '')


    def draw_plot(self,bool):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index(['Date'], inplace=True)
        self.data = self.data.astype(float)
        plot_data=self.data.iloc[self.start:self.end]
        add_plot=[]
        #需要以**kw形式传参，再一个个匹配公式
        other = self.data.loc[:,'Close'].to_frame()
        other['ma']=other['Close'].rolling(window=5).mean()
        other['diff']=other['Close'].rolling(window=bool).std()
        other['upper']=other.apply(lambda x : x['ma'] + 2 * x['diff'],axis=1)
        other['lower']=other.apply(lambda x : x['ma'] - 2 * x['diff'],axis=1)
        add_plot.append(mpf.make_addplot(other['upper'].iloc[self.start:self.end]))
        add_plot.append(mpf.make_addplot(other['ma'].iloc[self.start:self.end]))
        add_plot.append(mpf.make_addplot(other['lower'].iloc[self.start:self.end]))
        mpf.plot(  plot_data
                 # , ax=self.ax1
                 , addplot=add_plot
                 , type='candle'
                 # , title='SimplePic'
                 # , mav=(5, 21)
                 , style=self.my_style
                 # , volume=self.ax2
                 , volume=True
                 , datetime_format='%Y-%m'
                 , xrotation=0
                 , figsize=(12,8)
                )
        # self.fig.show()
    # def on_press(self):
    #
    # def on_motion(self):
    #
    # def on_release(self):
