#encoding=utf-8
import mplfinance as mpf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
class InterCandle:
    def __init__(self, data, my_style):
        self.data=data
        self.style=my_style
        self.idx_start=0
        self.press=False
        self.xpress=None
        self.fig = mpf.figure(style=my_style, figsize=(12, 8), facecolor=(0.82, 0.83, 0.85),dpi=100)
        fig = self.fig
        self.ax1 = fig.add_axes([0.08, 0.25, 0.88, 0.60])
        self.ax2 = fig.add_axes([0.08, 0.15, 0.88, 0.10], sharex=self.ax1)
        self.ax1.set_ylabel('Price')
        self.ax2.set_ylabel('Volume')
        # self.t1= fig.text(0.50, 0.94, 'sh.600000:')
        # self.t2= fig.text(0.12, 0.89, 'Open/Close: ', **normal_label_font)
        # self.t3= fig.text(0.14, 0.89, '')
        # self.t4= fig.text(0.12, 0.86, '')
        # self.t5= fig.text(0.40, 0.90, 'High: ', **normal_label_font)
        # self.t6= fig.text(0.40, 0.90, '')
        # self.t7= fig.text(0.40, 0.86, 'Low: ', **normal_label_font)
        # self.t8= fig.text(0.40, 0.86, '')
        # self.t9= fig.text(0.55, 0.90, 'Volum(M): ', **normal_label_font)
        # self.t10= fig.text(0.55, 0.90, '')
        fig.canvas.mpl_connect('button_press_event', self.on_press)
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def refresh_plot(self,idx_start):
        all_data = self.data
        plot_data = all_data.iloc[idx_start:idx_start + 100]
        mpf.plot(plot_data,
                 ax=self.ax1,
                 volume=self.ax2,
                 type='candle',
                 # datetime_format='%Y-%m',
                 # xrotation=0)
                 )
        mpl.use('TkAgg')
        # plt.switch_backend('gtk3agg')
        self.fig.show()

    def on_press(self,event):
        if not event.inaxes ==self.ax1:
            return
        if event.button != 1:
            return
        self.pressed = True
        self.xpress = event.xdata

    def on_motion(self, event):
        if not self.pressed:
            return
            # 如果移动出了ax1的范围，也退出处理函数
        if not event.inaxes == self.ax1:
            return
            # 如果鼠标在ax1范围内，且左键按下，则开始计算dx，并根据dx计算新的K线图起点
        dx = int(event.xdata - self.xpress)
        new_start = self.idx_start - dx
        if new_start <= 0:
            new_start = 0
        if new_start >= len(self.data) - 100:
            new_start = len(self.data) - 100
        self.ax1.clear()
        self.ax2.clear()
        self.refresh_plot(new_start)

    def on_release(self, event):
        # 按键释放后，设置鼠标的pressed为False
        self.pressed = False
        # 此时别忘了最后一次更新K线图的起点，否则下次拖拽的时候就不会从这次的起点开始移动了
        dx = int(event.xdata - self.xpress)
        self.idx_start -= dx
        if self.idx_start <= 0:
            self.idx_start = 0
        if self.idx_start >= len(self.data) - 100:
            self.idx_start = len(self.data) - 100
