from pyb import UART

header1 = 0x2C
header2 = 7
color = 0
direction = 0
angle = 0
isOpen = 0
end = 0x5B
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)  # 8位数据位，无校验位，1位停止位


def sendData():
    allData = [header1, header2, color, direction, angle, isOpen, end]
    datas = bytearray(allData)
    uart.write(datas)
