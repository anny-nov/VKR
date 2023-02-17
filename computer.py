from dataclasses import dataclass


@dataclass
class Computer:
    name: str
    hardware_id: str
    cpu: str
    gpus: list
    disks: list
    ram: int


