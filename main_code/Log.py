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

    def parse_data(self):
        if(self.type == 0):
            self.data = self.data["processes"]
        elif(self.type==1):
            pass
        elif(self.type==2):
            pass
        elif(self.type==3):
            pass
        elif(self.type == 5):
            self.data = self.data["browser_history"]

    def parse_time(self):
        self.datetime = datetime.datetime.fromtimestamp(self.timestamp)
        print(self.datetime)
