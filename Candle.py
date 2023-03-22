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

    def draw_plot(self,bool):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index(['Date'], inplace=True)
        self.data = self.data.astype(float)
        self.add_plot=[]
        #需要以**kw形式传参，再一个个匹配公式
        self.other = self.data.loc[:,'Close'].to_frame()
        self.other['ma']=self.other['Close'].rolling(window=bool).mean()
        self.other['diff']=self.other['Close'].rolling(window=bool).std()
        self.other['upper']=self.other.apply(lambda x : x['ma'] + 2 * x['diff'],axis=1)
        self.other['lower']=self.other.apply(lambda x : x['ma'] - 2 * x['diff'],axis=1)
        self.add_plot.append(mpf.make_addplot(self.other['upper'].iloc[self.start:self.end]))
        self.add_plot.append(mpf.make_addplot(self.other['ma'].iloc[self.start:self.end]))
        self.add_plot.append(mpf.make_addplot(self.other['lower'].iloc[self.start:self.end]))
        mpf.plot(self.data.iloc[self.start:self.end]
                 , addplot=self.add_plot
                 , type='candle'
                 , ylabel='price'
                 , style=self.my_style
                 , title='SimplePic'
                 # , mav=(5, 21)
                 , volume=True
                 , figratio=(16, 8)
                 , figscale=2)
    # def on_press(self):
    #
    # def on_motion(self):
    #
    # def on_release(self):
