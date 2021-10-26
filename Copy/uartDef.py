# 串口相关
from pyb import UART
import colorDef as CD

uart = UART(3, 115200)

uart.init(115200, bits=8, parity=None, stop=1)  # 8位数据位，无校验位，1位停止位

def uartData(color):
    """发送颜色信息

    Args:
         color (字符串): 期待发送的颜色
    """
    temp = 0
    if color == 'black':
        temp = CD.black
    elif color == 'brown':
        temp = CD.brown
    elif color == 'red':
        temp = CD.red
    elif color == 'green':
        temp = CD.green
    elif color == 'yellow':
        temp = CD.yellow
    elif color == 'blue':
        temp = CD.blue
    data = bytearray([0x2C, 4, temp, 0x5B])
    uart.write(data)
