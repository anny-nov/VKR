from datetime import datetime, date

import requests
import pyqtgraph as pg

from Log import Log
from main_code.Access import get_api_key

API_KEY = ''

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [str(datetime.fromtimestamp(value)) for value in values]

class Chart():
    def __init__(self, hardware_id, ram, start=0, finish=0):
        if start == 0:
            dt = datetime.combine(date.today(), datetime.min.time())
            self.start = int(datetime.timestamp(dt))
        else:
            self.start = start
        if finish == 0:
            self.finish = int(datetime.timestamp(datetime.now()))
        else:
            self.finish = finish
        self.hardware_id = hardware_id
        self.max_ram = ram

    def get_gata(self):
        global API_KEY
        API_KEY = get_api_key()
        api_url = 'http://afire.tech:5000/api/log?hardware_id=' + self.hardware_id + '&from=' + str(
            self.start) + '&to=' + str(self.finish) + '&type=1&api_key=' + API_KEY
        print(api_url)
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
            y=self.cpus, pen=pen
        )
        self.cpu_plot_widget.setBackground('w')
        self.cpu_plot_widget.setYRange(0, 1)
        return self.cpu_plot_widget

    def draw_ram_chart(self):
        self.date_axis = TimeAxisItem(orientation='bottom')
        self.ram_plot_widget = pg.PlotWidget(
            axisItems={'bottom': self.date_axis},
            title='<h2>RAM Load</h2>'
        )
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.ram_plot_widget.plot(
            x=[x.timestamp() for x in self.times],
            y=self.rams, pen=pen
        )
        self.ram_plot_widget.setBackground('w')
        self.ram_plot_widget.setYRange(0, int(self.max_ram))
        return self.ram_plot_widget
