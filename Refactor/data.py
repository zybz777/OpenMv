# 传输数据定义相关 - By: zyb - 周一 10月 25 2021
from pyb import UART

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)  # 8位数据位，无校验位，1位停止位
""" ------ 数据定义 全局变量 ------ """
header1 = 0x2C
header2 = 8
color = 0
direction = 0
angle = 0
isOpen = 0
ball = 0
end = 0x5B


def setData(data, target):
    """ 写入数据 """
    global color
    global direction
    global angle
    global isOpen
    global ball

    if target == 'color':
        color = data
    elif target == 'direction':
        direction = data
    elif target == 'angle':
        angle = data
    elif target == 'isOpen':
        isOpen = data
    elif target == 'ball':
        ball = data


def clearData():
    """ 数据复位 """
    global color
    global direction
    global angle
    global isOpen
    global ball

    color = 0
    direction = 0
    angle = 0
    isOpen = 0
    ball = 0


def sendData():
    """ 数据发送 """
    allData = [header1, header2, color, direction, angle, isOpen, ball, end]
    # print(allData)
    datas = bytearray(allData)
    uart.write(datas)
