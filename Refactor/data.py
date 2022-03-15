# 传输数据定义相关 - By: zyb - 周一 10月 25 2021
from pyb import UART

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)  # 8位数据位，无校验位，1位停止位
""" ------ 数据定义 全局变量 ------ """
header1 = 100
header2 = 8
color = 0
direction = 0
angle = 0
isOpen = 0
ball = 0
end = 101
datasets = {
    'header1': 100,
    'header2': 8,
    'color': 0,
    'direction': 0,
    'angle': 0,
    'isOpen': 0,
    'ball': 0,
    'end': 101
}


def set_data(data, target):
    """写入待发送数据

    Args:
        data (_type_): 要发送的数据
        target (str): 对用的位置, 查看datasets的具体定义
    """
    global datasets
    datasets[target] = data


def clear_data():
    """ 数据复位 """
    global datasets

    datasets['color'] = 0
    datasets['direction'] = 0
    datasets['angle'] = 0
    datasets['isOpen'] = 0
    datasets['ball'] = 0


def send_data():
    """ 数据发送 """
    allData = []
    #for data in datasets.values():
        #allData.append(data)
    allData.append(datasets['header1'])
    allData.append(datasets['header2'])
    allData.append(datasets['color'])
    allData.append(datasets['direction'])
    allData.append(datasets['angle'])
    allData.append(datasets['isOpen'])
    allData.append(datasets['ball'])
    allData.append(datasets['end'])
    #print(allData)
    datas = bytearray(allData)
    uart.write(datas)


def reveive_data():
    info = '0'
    if uart.any():
        info = uart.readline().decode()
    return info

