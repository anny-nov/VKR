import datetime
import json
from dataclasses import dataclass


@dataclass
class Log:
    id: int
    hardware_id: str
    type: int
    timestamp: int
    data: dict

    def parse_time(self):
        self.datetime = datetime.datetime.fromtimestamp(self.timestamp)

    def get_load(self):
        self.cpu = str(self.data['cpu'])
        self.cpu = float(self.cpu.replace('%', ''))
        self.ram = str(self.data['ram'])
        self.ram = int(self.ram.replace('MB', ''))
        print('ram ', self.ram, 'cpu ', self.cpu)
