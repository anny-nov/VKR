from datetime import datetime

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel, \
    QListWidget, QListWidgetItem, QMenu, QGridLayout, QDateEdit, QHBoxLayout, QComboBox, QMessageBox
from PyQt6.QtGui import QAction, QFont

from computer import Computer
import requests
from QTChat_copy import Chat_Widget
from main_code import menu
from main_code.Chart import Chart
from main_code.Log import Log
from main_code.LogCustomWidget import LogCustomQWidget
from main_code.Access import get_dec_key

API_KEY = ''

def parse_from_json(hardware_id):
    api_url = 'http://46.151.30.76:5000/api/computer?hardware_id=' + hardware_id + '&api_key=' + API_KEY
    comp_json = requests.get(api_url)
    comp_dict = comp_json.json()
    comp_info = Computer(**comp_dict)
    return comp_info

def parse_log(hardware_id):
    api_url = 'http://afire.tech:5000/api/log?hardware_id=' + hardware_id + '&api_key=' + API_KEY
    log_list_json = requests.get(api_url)
    log_list_dict = log_list_json.json()
    log_list_dict = log_list_dict['logs']
    log_list = list()
    for el in log_list_dict:
        tmp = Log(**el)
        tmp.parse_time()
        log_list.append(tmp)
    return log_list

def parse_logs_with_filters(hardware_id,from_timestamp,to_timestamp,log_type):
    api_url=''
    if(log_type == 5):
        api_url = 'http://afire.tech:5000/api/log?hardware_id=' + hardware_id + '&from=' + str(
            from_timestamp) + '&to=' + str(to_timestamp) + '&api_key=' + API_KEY
    else:
        if(log_type == 4):
            log_type+=1
        api_url = 'http://afire.tech:5000/api/log?hardware_id=' + hardware_id + '&from=' + str(
            from_timestamp) + '&to=' + str(to_timestamp) + '&type=' + str(log_type) + '&api_key=' + API_KEY
    print(api_url)
    log_list_json = requests.get(api_url)
    log_list_dict = log_list_json.json()
    log_list_dict = log_list_dict['logs']
    log_list = list()
    for el in log_list_dict:
        tmp = Log(**el)
        tmp.parse_time()
        log_list.append(tmp)
    return log_list


class ComputerInfoWindow(QMainWindow):
    def __init__(self, hardware_id, parent=None):
        super().__init__(parent)
        self.log_type = None
        global API_KEY
        API_KEY = get_dec_key()
        self.comp_info = parse_from_json(hardware_id)
        self.logs = parse_log(hardware_id)
        self.initUI()
        self._createMenuBar()
        self.index = 0

    def initUI(self):
        self.setWindowTitle("Detailed information about computer")
        self.setMinimumSize(QSize(600, 600))
        self.grid = QGridLayout()

        ComputerName = QLabel(self.comp_info.name)
        font = QFont()
        font.setPointSize(14)
        ComputerName.setFont(font)
        ComputerId = QLabel('Hardware ID: ' + self.comp_info.hardware_id)
        CpuInfo = QLabel('CPU: ' + self.comp_info.cpu)
        OSInfo = QLabel('OS: ' + self.comp_info.OS)
        RamInfo = QLabel('RAM: ' + str(self.comp_info.ram) + 'MB')
        DisksHeader = QLabel('Hard disks: ')
        Gpusheader = QLabel('GPUs: ')
        ChartsHeader = QLabel('Metriks of computer')
        ChartsHeader.setFont(font)
        headers_font = QFont()
        headers_font.setPointSize(14)
        DisksHeader.setFont(headers_font)
        Gpusheader.setFont(headers_font)

        disks_list = QListWidget()
        disks_list.setMaximumSize(400, 100)
        gpus_list = QListWidget()
        gpus_list.setMaximumSize(400, 100)
        for el in self.comp_info.disks:
            disks_list.addItem(el)
        for el in self.comp_info.gpus:
            gpus_list.addItem(el)

        chat_class = Chat_Widget()
        chat = chat_class.initLayout()

        from_label = QLabel('From')
        from_label.setMaximumSize(50, 20)
        to_label = QLabel('To')
        to_label.setMaximumSize(40, 20)
        self.from_time_widget = QDateEdit()
        self.to_time_widget = QDateEdit()
        self.to_time_widget.setDate(datetime.today())
        self.from_time_widget.setDate(datetime.today())
        self.to_time_widget.setMaximumDate(datetime.today())
        self.from_time_widget.setMaximumDate(datetime.today())
        self.from_time_widget.setMinimumDate(datetime.fromtimestamp(0))
        self.to_time_widget.setMinimumDate(datetime.fromtimestamp(0))
        type_label = QLabel('Log Type')
        type_label.setMaximumSize(70, 20)
        self.type_filter = QComboBox()
        self.type_filter.addItems(['PROCESS', 'LOAD', 'USB_DEVICE', 'NEW_CONFIGURATION', 'BROWSER', 'ALL'])
        self.type_filter.currentIndexChanged.connect(self.GetType)
        filter_button = QPushButton('Apply filter')
        filter_button.clicked.connect(self.filter)

        time_layout = QHBoxLayout()
        time_layout.setSpacing(5)
        time_layout.addWidget(from_label)
        time_layout.addWidget(self.from_time_widget)
        time_layout.addWidget(to_label)
        time_layout.addWidget(self.to_time_widget)
        time_layout.addWidget(type_label)
        time_layout.addWidget(self.type_filter)
        time_layout.addWidget(filter_button)
        self.logs = parse_log(self.comp_info.hardware_id)
        self.CreateLogListWidget()


        self.charts = Chart(self.comp_info.hardware_id, self.comp_info.ram)
        self.charts.get_gata()
        self.cpu_chart = self.charts.draw_cpu_chart()
        self.ram_chart = self.charts.draw_ram_chart()
        chart_from_label = QLabel('From')
        chart_from_label.setMaximumSize(50, 20)
        chart_to_label = QLabel('To')
        chart_to_label.setMaximumSize(40, 20)
        self.chart_from_time_widget = QDateEdit()
        self.chart_to_time_widget = QDateEdit()
        self.chart_to_time_widget.setDate(datetime.today())
        self.chart_from_time_widget.setDate(datetime.today())
        self.chart_to_time_widget.setMaximumDate(datetime.today())
        self.chart_from_time_widget.setMaximumDate(datetime.today())
        self.chart_from_time_widget.setMinimumDate(datetime.fromtimestamp(0))
        self.chart_to_time_widget.setMinimumDate(datetime.fromtimestamp(0))
        chart_filter_button = QPushButton('Update')
        chart_filter_button.clicked.connect(self.update_charts)

        chart_time_layout = QHBoxLayout()
        chart_time_layout.setSpacing(5)
        chart_time_layout.addWidget(chart_from_label)
        chart_time_layout.addWidget(self.chart_from_time_widget)
        chart_time_layout.addWidget(chart_to_label)
        chart_time_layout.addWidget(self.chart_to_time_widget)
        chart_time_layout.addWidget(chart_filter_button)

        self.grid.addWidget(self.logListWidget, 11, 0, 9, 2)
        self.grid.addLayout(time_layout, 20, 0, 1, 2)
        self.grid.addLayout(chat, 0, 0, 10, 2)
        self.grid.addWidget(ComputerName, 0, 3, 1, 2)
        self.grid.addWidget(ComputerId, 1, 3, 1, 2)
        self.grid.addWidget(OSInfo, 2, 3, 1, 2)
        self.grid.addWidget(CpuInfo, 3, 3, 1, 2)
        self.grid.addWidget(RamInfo, 4, 3, 1, 2)
        self.grid.addWidget(DisksHeader, 5, 3, 1, 2)
        self.grid.addWidget(disks_list, 6, 3, 1, 2)
        self.grid.addWidget(Gpusheader, 7, 3, 1, 2)
        self.grid.addWidget(gpus_list, 8, 3, 1, 2)
        self.grid.addWidget(ChartsHeader, 9, 3, 1, 2)
        self.grid.addLayout(chart_time_layout, 10, 3, 1, 2)
        self.grid.addWidget(self.cpu_chart, 11, 3, 4, 2)
        self.grid.addWidget(self.ram_chart, 16, 3, 4, 2)
        self.grid.setRowStretch(self.grid.rowCount(), 1)

        view = QWidget(self)
        self.setCentralWidget(view)
        view.setLayout(self.grid)

    def _createMenuBar(self):
        self.all_menu = self.menuBar()
        mamangement_menu = QMenu("Management", self)
        self.all_menu.addMenu(mamangement_menu)
        actions_menu = self.all_menu.addMenu("Actions")
        self.all_menu.addMenu(actions_menu)

        NewMobileAPIAction = QAction('New mobile API key', self)
        NewMobileAPIAction.setStatusTip('Release new API key to connect mobile app')
        NewMobileAPIAction.triggered.connect(menu.new_APIKey)
        mamangement_menu.addAction(NewMobileAPIAction)

        DeleteAction = QAction('Delete computer', self)
        DeleteAction.setStatusTip('Completely delete information about computer from database')
        DeleteAction.triggered.connect(lambda: menu.DeleteComputer(self, self.comp_info.hardware_id))
        actions_menu.addAction(DeleteAction)

    def CreateLogListWidget(self):
        self.logListWidget = QListWidget()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fillLogListWidget)
        self.timer.start(50)

    def fillLogListWidget(self):
        if self.index < len(self.logs):
            if self.logs[self.index].type == 1:
                self.index += 1
            else:
                LogLineWidget = LogCustomQWidget()
                LogLineWidget.setText(str(self.logs[self.index].data))
                LogLineWidget.setTime(str(self.logs[self.index].datetime))
                LogLineWidget.setIcon(self.logs[self.index].type)
                LogLineWidget.setId(self.logs[self.index].id)
                LogLineWidget.setHardwareId(self.logs[self.index].hardware_id)
                logListWidgetItem = QListWidgetItem(self.logListWidget)
                logListWidgetItem.setSizeHint(LogLineWidget.sizeHint())
                self.logListWidget.addItem(logListWidgetItem)
                self.logListWidget.setItemWidget(logListWidgetItem, LogLineWidget)
                self.index += 1
        if self.index >= len(self.logs):
            self.timer.stop()
            self.index = 0

    def update_charts(self):
        to_time = int(datetime.timestamp(self.chart_to_time_widget.dateTime().toPyDateTime()))
        from_time = int(datetime.timestamp(self.chart_from_time_widget.dateTime().toPyDateTime()))
        if (to_time>=from_time):
            self.cpu_chart.close()
            self.ram_chart.close()
            self.charts = Chart(self.comp_info.hardware_id, self.comp_info.ram, from_time, to_time)
            self.charts.get_gata()
            self.cpu_chart = self.charts.draw_cpu_chart()
            self.ram_chart = self.charts.draw_ram_chart()
            self.grid.addWidget(self.cpu_chart, 11, 3, 4, 2)
            self.grid.addWidget(self.ram_chart, 16, 3, 4, 2)
            self.grid.update()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Filter error")
            msg.setText("Date setting is invalid")
            #msg.setIcon(QMessageBox.warning)
            msg.exec()

    def GetType(self, type):
        self.log_type = type

    def filter(self):
        to_time = int(datetime.timestamp(self.to_time_widget.dateTime().toPyDateTime()))
        from_time = int(datetime.timestamp(self.from_time_widget.dateTime().toPyDateTime()))
        if (to_time >= from_time):
            self.logs = parse_logs_with_filters(self.comp_info.hardware_id, from_time, to_time, self.log_type)
            self.logListWidget.clear()
            self.CreateLogListWidget()
            self.grid.addWidget(self.logListWidget, 6, 0, 7, 2)
            self.grid.update()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Filter error")
            msg.setText("Date setting is invalid")
            #msg.setIcon(QMessageBox.Warning)
            msg.exec()
