from datetime import datetime

import matplotlib.pyplot as plt
import requests
import pyqtgraph as pg

from Log import Log
from main_code.Access import get_api_key

API_KEY = ''

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

class Chart():
    def __init__(self, hardware_id, start=0, finish=0):
        if start == 0:
            self.start = datetime(datetime.today())
            self.start = datetime.timestamp(self.start)
        else:
            self.start = start
        if finish == 0:
            self.finish = datetime.now()
            self.start = datetime.timestamp(self.start)
        else:
            self.finish = finish
        self.hardware_id = hardware_id

    def get_gata(self):
        global API_KEY
        API_KEY = get_api_key()
        api_url = 'http://afire.tech:5000/api/log?hardware_id=' + self.hardware_id + '&from=' + str(
            self.start) + '&to=' + str(self.finish) + '&type=1&api_key=' + API_KEY
        log_list_json = requests.get(api_url)
        log_list_dict = log_list_json.json()
        log_list_dict = log_list_dict['logs']
        self.cpus = list()
        self.rams = list()
        self.times = list()
        for el in log_list_dict:
            tmp = Log(**el)
            tmp.parse_time()
            tmp.get_load()
            self.cpus.append(tmp.cpu)
            self.rams.append(tmp.ram)
            self.times.append(tmp.datetime)
        print(self.times)

    def draw_cpu_chart(self):
        self.date_axis = TimeAxisItem(orientation='bottom')
        self.cpu_plot_widget = pg.PlotWidget(
            axisItems={'bottom': self.date_axis},
            title='<h2>CPU Load</h2>'
        )
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.cpu_plot_widget.plot(
            x=[x.timestamp() for x in self.times],
            y=self.cpus, pen=pen, symbol='o'
        )
        return self.cpu_plot_widget
        #fig = plt.figure()
        #time_data_float = matplotlib.dates.date2num(self.times)
        #pylab.plot_date(time_data_float, self.cpus, fmt="b-")
        #axes = pylab.subplot(1, 1, 1)
        #axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y-%m-%d %H:%M"))
        #axes.set_xticklabels(self.times, rotation=45, ha='right')
        #pylab.grid()
        #pylab.show()
