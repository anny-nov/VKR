class Computer:
    def __init__(self,info_dict):
        self.name = info_dict['name']
        self.hardware_id = info_dict['hardware_id']
        self.cpu = info_dict['cpu']
        self.gpus = info_dict['gpus']
        self.ram = info_dict['ram']
        self.disks = info_dict['disks']
