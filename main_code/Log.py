from dataclasses import dataclass


@dataclass
class Log:
    id: int
    hardware_id: str
    type: int
    timestamp: int
    data: str
