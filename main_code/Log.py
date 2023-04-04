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
