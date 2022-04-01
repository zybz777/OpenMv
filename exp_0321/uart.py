from pyb import UART
from utils import COLOR


class Uart():
    def __init__(self):
        self.uart = UART(3, 115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)
        self.datasets = {'header1': 100, 'header2': 8, 'color': 0, 'direction': 0, 'angle': 0, 'isOpen': 0, 'ball': 0, 'end': 101}

    def set_data(self, data_value, data_position):
        self.datasets[data_position] = data_value

    def clear_data(self):
        self.datasets['color'] = 0
        self.datasets['direction'] = 0
        self.datasets['angle'] = 0
        self.datasets['isOpen'] = 0
        self.datasets['ball'] = 0

    def send_data(self):
        allData = []
        # for 遍历字典 append 顺序会乱
        allData.append(self.datasets['header1'])
        allData.append(self.datasets['header2'])
        allData.append(self.datasets['color'])
        allData.append(self.datasets['direction'])
        allData.append(self.datasets['angle'])
        allData.append(self.datasets['isOpen'])
        allData.append(self.datasets['ball'])
        allData.append(self.datasets['end'])
        datas = bytearray(allData)
        self.uart.write(datas)

    def reveive_data(self):
        info = '0'
        if self.uart.any():
            info = self.uart.readline().decode()  # 1 2 3 4 5 6 7
        return info


my_uart = Uart()
